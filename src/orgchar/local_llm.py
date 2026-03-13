"""
Local LLM implementation for OrgChar when OpenAI API is unavailable
"""

import logging
from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from transformers import pipeline

logger = logging.getLogger(__name__)

class LocalLLMAdapter:
    """Adapter for using local LLMs with the RAG system."""
    
    def __init__(self, model_name: str = "google/flan-t5-base", max_new_tokens: int = 512):
        """
        Initialize the local LLM adapter.
        
        Args:
            model_name: Name of the Hugging Face model to use
            max_new_tokens: Maximum tokens to generate per response
        """
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.pipeline = None
        
        # Initialize the model
        self._initialize_model()
        
        # Create prompt template
        self.prompt_template = PromptTemplate.from_template(
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

    @property
    def is_available(self) -> bool:
        """Whether the local LLM backend is ready to serve requests."""
        return self.pipeline is not None
    
    def _initialize_model(self):
        """Initialize the local LLM."""
        try:
            logger.info(f"Loading local LLM model: {self.model_name}")
            
            # Create HuggingFace pipeline
            self.pipeline = pipeline(
                "text2text-generation",
                model=self.model_name,
                max_new_tokens=self.max_new_tokens
            )
            
            logger.info("Local LLM initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize local LLM: {e}")
            self.pipeline = None
    
    def generate_answer(self, question: str, context_docs: List[Document]) -> str:
        """
        Generate an answer using the local LLM and retrieved context.
        
        Args:
            question: User question
            context_docs: Retrieved context documents
            
        Returns:
            Generated answer
        """
        if not self.pipeline:
            return "Error: Local LLM not initialized properly."
        
        try:
            # Prepare context
            context = "\n\n".join([
                f"Source: {doc.metadata.get('filename', 'Unknown')}\n{doc.page_content}"
                for doc in context_docs
            ])
            
            # Format prompt
            prompt = self.prompt_template.format(
                context=context,
                question=question
            )
            
            # Generate response
            generation = self.pipeline(prompt, max_new_tokens=self.max_new_tokens)
            if generation and isinstance(generation, list):
                text = generation[0].get("generated_text", "")
                return text.strip()
            return str(generation)
            
        except Exception as e:
            logger.error(f"Failed to generate answer with local LLM: {e}")
            return f"Error generating answer with local LLM: {str(e)}"
