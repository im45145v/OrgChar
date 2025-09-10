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
    
    # Try to use OpenAI
    rag_system = RAGSystem(config)
    success = rag_system.load_knowledge_base()
    
    if not success:
        logger.error("Failed to load knowledge base")
        return
    
    # Test if OpenAI API is working
    try:
        test_response = rag_system.answer_question("Test question")
        if "Error" in test_response.get('answer', '') and "API" in test_response.get('answer', ''):
            logger.warning("OpenAI API not available, falling back to local LLM")
            use_local_llm()
        else:
            logger.info("OpenAI API is working, starting app normally")
            run_normal()
    except Exception as e:
        logger.warning(f"Error testing OpenAI API: {e}, falling back to local LLM")
        use_local_llm()

def run_normal():
    """Run the application with OpenAI."""
    os.system("streamlit run app.py")

def use_local_llm():
    """Run the application with local LLM."""
    logger.info("Starting with local LLM fallback...")
    
    # This would require modifying rag_system.py to use local_llm.py
    # For now, we'll just use the offline demo
    os.system("streamlit run app_offline.py")
    
    # Inform the user
    print("\n" + "="*50)
    print("RUNNING IN OFFLINE MODE DUE TO OPENAI API ISSUES")
    print("="*50)
    print("\nTo use a local LLM instead, modify rag_system.py to use the LocalLLMAdapter")
    print("See local_llm.py for implementation details")
    print("\nTo use OpenAI again, update your API key in the .env file")

if __name__ == "__main__":
    main()
