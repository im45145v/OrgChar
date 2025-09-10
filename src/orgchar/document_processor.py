"""
Document processing module for handling PDF and text documents.
"""

import os
import logging
from pathlib import Path
from typing import List, Optional
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document loading, processing, and chunking."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Maximum size of text chunks
            chunk_overlap: Overlap between chunks for context preservation
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_pdf(self, file_path: Path) -> str:
        """
        Load and extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            Exception: If PDF reading fails
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            raise
    
    def load_text_file(self, file_path: Path) -> str:
        """
        Load text from a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File content as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            raise
    
    def load_documents_from_directory(self, directory_path: Path) -> List[Document]:
        """
        Load all supported documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of processed Document objects
        """
        documents = []
        supported_extensions = {'.pdf', '.txt', '.md'}
        
        if not directory_path.exists():
            logger.warning(f"Directory {directory_path} does not exist")
            return documents
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    if file_path.suffix.lower() == '.pdf':
                        content = self.load_pdf(file_path)
                    else:
                        content = self.load_text_file(file_path)
                    
                    if content.strip():
                        doc = Document(
                            page_content=content,
                            metadata={
                                'source': str(file_path),
                                'filename': file_path.name,
                                'type': file_path.suffix[1:].upper()
                            }
                        )
                        documents.append(doc)
                        logger.info(f"Loaded document: {file_path.name}")
                    else:
                        logger.warning(f"Empty document: {file_path.name}")
                        
                except Exception as e:
                    logger.error(f"Failed to load {file_path}: {e}")
        
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents
        """
        chunked_docs = []
        
        for doc in documents:
            chunks = self.text_splitter.split_text(doc.page_content)
            
            for i, chunk in enumerate(chunks):
                chunk_metadata = doc.metadata.copy()
                chunk_metadata['chunk_id'] = i
                chunk_metadata['total_chunks'] = len(chunks)
                
                chunked_doc = Document(
                    page_content=chunk,
                    metadata=chunk_metadata
                )
                chunked_docs.append(chunked_doc)
        
        logger.info(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
        return chunked_docs
    
    def process_directory(self, directory_path: Path) -> List[Document]:
        """
        Complete processing pipeline for a directory of documents.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of processed and chunked documents
        """
        logger.info(f"Processing documents from {directory_path}")
        
        # Load documents
        documents = self.load_documents_from_directory(directory_path)
        
        if not documents:
            logger.warning("No documents found to process")
            return []
        
        # Chunk documents
        chunked_documents = self.chunk_documents(documents)
        
        logger.info(f"Successfully processed {len(documents)} documents into {len(chunked_documents)} chunks")
        return chunked_documents