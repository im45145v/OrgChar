"""
OrgChar with Local LLM fallback
"""

import sys
import os
from pathlib import Path
import logging

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from orgchar.config import Config
from orgchar.rag_system import RAGSystem
from orgchar.local_llm import LocalLLMAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run OrgChar with local LLM fallback."""
    config = Config()
    config.ensure_directories()

    rag_system = RAGSystem(config)
    success = rag_system.load_knowledge_base()

    if not success:
        logger.error("Failed to load knowledge base")
        return

    if rag_system.backend in {"openai", "local"}:
        logger.info(f"Starting app with backend: {rag_system.backend}")
        run_normal()
    else:
        logger.warning("No LLM backend available, using offline mode")
        use_local_llm()

def run_normal():
    """Run the application with OpenAI."""
    os.system("streamlit run app.py")

def use_local_llm():
    """Run the application with local LLM."""
    logger.info("Starting offline demo mode...")

    # If no local backend is available, switch to offline demo mode.
    os.system("streamlit run app_offline.py")

    # Inform the user
    print("\n" + "="*50)
    print("RUNNING IN OFFLINE DEMO MODE")
    print("="*50)
    print("\nRAGSystem supports LocalLLMAdapter when configured and available.")
    print("Current runtime was unable to initialize an online/local backend, so demo mode is used.")
    print("\nTo use OpenAI again, update your API key in the .env file")

if __name__ == "__main__":
    main()
