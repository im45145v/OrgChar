"""
Configuration module for OrgChar RAG chatbot.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for OrgChar application."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
    
    # Paths
    KNOWLEDGE_BASE_PATH = Path(os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base"))
    VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", "./vector_db"))
    
    # Document processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    
    # Model configuration
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    
    # Streamlit configuration
    STREAMLIT_PAGE_TITLE = "OrgChar - Organizational Behavior Chatbot"
    STREAMLIT_PAGE_ICON = "🏢"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        cls.KNOWLEDGE_BASE_PATH.mkdir(parents=True, exist_ok=True)
        cls.VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)