"""
RAG (Retrieval-Augmented Generation) system for organizational behavior Q&A.
"""

import logging
from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from .vector_store import VectorStore
from .config import Config

logger = logging.getLogger(__name__)

class RAGSystem:
    """Main RAG system for question answering using retrieved documents."""
    
    def __init__(self, config: Config = None):
        """
        Initialize the RAG system.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config()
        
        # Initialize components
        self.vector_store = VectorStore(embedding_model=self.config.EMBEDDING_MODEL)
        self.llm = ChatOpenAI(
            model=self.config.LLM_MODEL,
            temperature=self.config.TEMPERATURE,
            openai_api_key=self.config.OPENAI_API_KEY
        ) if self.config.OPENAI_API_KEY else None
        
        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_template(
            """You are an expert in organizational behavior and management. Use the following context to answer the question about organizational behavior, workplace dynamics, leadership, or related topics.

Context from knowledge base:
{context}

Question: {question}

Instructions:
1. Provide a comprehensive and accurate answer based on the context provided
2. If the context doesn't contain enough information, clearly state what information is missing
3. Focus on practical applications and real-world examples when relevant
4. Cite specific concepts or frameworks from the context when applicable
5. If no relevant context is found, provide a general response based on your knowledge of organizational behavior

Answer:"""
        )
    
    def load_knowledge_base(self, force_rebuild: bool = False) -> bool:
        """
        Load or rebuild the knowledge base from documents.
        
        Args:
            force_rebuild: Whether to force rebuilding the index
            
        Returns:
            True if knowledge base loaded/built successfully
        """
        vector_db_path = self.config.VECTOR_DB_PATH
        
        # Try to load existing index first
        if not force_rebuild and self.vector_store.load_index(vector_db_path):
            logger.info("Loaded existing knowledge base")
            return True
        
        # Rebuild index from documents
        logger.info("Building knowledge base from documents...")
        return self._rebuild_knowledge_base()
    
    def _rebuild_knowledge_base(self) -> bool:
        """
        Rebuild the knowledge base from scratch.
        
        Returns:
            True if rebuild successful
        """
        try:
            from .document_processor import DocumentProcessor
            
            # Process documents
            processor = DocumentProcessor(
                chunk_size=self.config.CHUNK_SIZE,
                chunk_overlap=self.config.CHUNK_OVERLAP
            )
            
            documents = processor.process_directory(self.config.KNOWLEDGE_BASE_PATH)
            
            if not documents:
                logger.warning("No documents found in knowledge base directory")
                return False
            
            # Create vector index
            self.vector_store.create_index(documents)
            
            # Save index
            self.vector_store.save_index(self.config.VECTOR_DB_PATH)
            
            logger.info(f"Knowledge base built with {len(documents)} document chunks")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rebuild knowledge base: {e}")
            return False
    
    def add_documents_to_knowledge_base(self, documents: List[Document]) -> bool:
        """
        Add new documents to the existing knowledge base.
        
        Args:
            documents: List of documents to add
            
        Returns:
            True if documents added successfully
        """
        try:
            self.vector_store.add_documents(documents)
            self.vector_store.save_index(self.config.VECTOR_DB_PATH)
            logger.info(f"Added {len(documents)} documents to knowledge base")
            return True
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def retrieve_context(self, query: str, k: int = 4) -> List[Document]:
        """
        Retrieve relevant context documents for a query.
        
        Args:
            query: User question or query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"Failed to retrieve context: {e}")
            return []
    
    def generate_answer(self, question: str, context_docs: List[Document]) -> str:
        """
        Generate an answer using the LLM and retrieved context.
        
        Args:
            question: User question
            context_docs: Retrieved context documents
            
        Returns:
            Generated answer
        """
        if not self.llm:
            return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY in your environment."
        
        try:
            # Prepare context
            context = "\n\n".join([
                f"Source: {doc.metadata.get('filename', 'Unknown')}\n{doc.page_content}"
                for doc in context_docs
            ])
            
            # Generate response
            messages = self.prompt_template.format_messages(
                context=context,
                question=question
            )
            
            response = self.llm(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            return f"Error generating answer: {str(e)}"
    
    def answer_question(self, question: str, retrieve_k: int = 4) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve context and generate answer.
        
        Args:
            question: User question
            retrieve_k: Number of context documents to retrieve
            
        Returns:
            Dictionary containing answer and metadata
        """
        try:
            # Retrieve context
            context_docs = self.retrieve_context(question, k=retrieve_k)
            
            # Generate answer
            answer = self.generate_answer(question, context_docs)
            
            # Prepare response
            sources = []
            for doc in context_docs:
                source_info = {
                    'filename': doc.metadata.get('filename', 'Unknown'),
                    'type': doc.metadata.get('type', 'Unknown'),
                    'chunk_id': doc.metadata.get('chunk_id', 0)
                }
                if source_info not in sources:
                    sources.append(source_info)
            
            return {
                'answer': answer,
                'sources': sources,
                'context_count': len(context_docs),
                'question': question
            }
            
        except Exception as e:
            logger.error(f"Failed to answer question: {e}")
            return {
                'answer': f"Error processing question: {str(e)}",
                'sources': [],
                'context_count': 0,
                'question': question
            }
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current knowledge base.
        
        Returns:
            Dictionary containing knowledge base statistics
        """
        return self.vector_store.get_stats()
    
    def update_knowledge_base(self) -> bool:
        """
        Update the knowledge base by reprocessing all documents.
        
        Returns:
            True if update successful
        """
        logger.info("Updating knowledge base...")
        return self._rebuild_knowledge_base()