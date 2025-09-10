"""
Vector store module for managing document embeddings and similarity search.
"""

import logging
import pickle
from pathlib import Path
from typing import List, Tuple, Optional
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

logger = logging.getLogger(__name__)

class VectorStore:
    """Manages document embeddings and similarity search using FAISS."""
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the vector store.
        
        Args:
            embedding_model: Name of the sentence transformer model to use
        """
        self.embedding_model = embedding_model
        self.embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
        self.vector_store: Optional[FAISS] = None
        
    def create_index(self, documents: List[Document]) -> None:
        """
        Create a new vector index from documents.
        
        Args:
            documents: List of documents to index
        """
        if not documents:
            logger.warning("No documents provided for indexing")
            return
        
        logger.info(f"Creating vector index for {len(documents)} documents")
        
        try:
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            logger.info("Vector index created successfully")
        except Exception as e:
            logger.error(f"Failed to create vector index: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add new documents to existing vector store.
        
        Args:
            documents: List of documents to add
        """
        if not documents:
            logger.warning("No documents provided for adding")
            return
        
        if self.vector_store is None:
            logger.info("No existing vector store, creating new one")
            self.create_index(documents)
            return
        
        try:
            logger.info(f"Adding {len(documents)} documents to existing index")
            self.vector_store.add_documents(documents)
            logger.info("Documents added successfully")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of similar documents
        """
        if self.vector_store is None:
            logger.warning("Vector store not initialized")
            return []
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.debug(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of tuples containing documents and their similarity scores
        """
        if self.vector_store is None:
            logger.warning("Vector store not initialized")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.debug(f"Found {len(results)} similar documents with scores for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Similarity search with score failed: {e}")
            return []
    
    def save_index(self, file_path: Path) -> None:
        """
        Save the vector store to disk.
        
        Args:
            file_path: Path to save the index
        """
        if self.vector_store is None:
            logger.warning("No vector store to save")
            return
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss_path = file_path / "faiss_index"
            self.vector_store.save_local(str(faiss_path))
            
            # Save metadata
            metadata_path = file_path / "metadata.pkl"
            metadata = {
                'embedding_model': self.embedding_model,
                'document_count': len(self.vector_store.docstore._dict)
            }
            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)
            
            logger.info(f"Vector store saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save vector store: {e}")
            raise
    
    def load_index(self, file_path: Path) -> bool:
        """
        Load a vector store from disk.
        
        Args:
            file_path: Path to load the index from
            
        Returns:
            True if loaded successfully, False otherwise
        """
        faiss_path = file_path / "faiss_index"
        metadata_path = file_path / "metadata.pkl"
        
        if not faiss_path.exists() or not metadata_path.exists():
            logger.warning(f"Vector store files not found at {file_path}")
            return False
        
        try:
            # Load metadata
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            
            # Verify embedding model compatibility
            if metadata.get('embedding_model') != self.embedding_model:
                logger.warning(f"Embedding model mismatch: expected {self.embedding_model}, "
                             f"found {metadata.get('embedding_model')}")
            
            # Load FAISS index
            self.vector_store = FAISS.load_local(
                str(faiss_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            logger.info(f"Vector store loaded from {file_path} with {metadata.get('document_count', 0)} documents")
            return True
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            return False
    
    def delete_index(self, file_path: Path) -> None:
        """
        Delete the vector store files from disk.
        
        Args:
            file_path: Path where the index is stored
        """
        try:
            if file_path.exists():
                import shutil
                shutil.rmtree(file_path)
                logger.info(f"Vector store deleted from {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete vector store: {e}")
    
    def get_stats(self) -> dict:
        """
        Get statistics about the current vector store.
        
        Returns:
            Dictionary containing vector store statistics
        """
        if self.vector_store is None:
            return {'status': 'not_initialized', 'document_count': 0}
        
        return {
            'status': 'initialized',
            'document_count': len(self.vector_store.docstore._dict),
            'embedding_model': self.embedding_model
        }