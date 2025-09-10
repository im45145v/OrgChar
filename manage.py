"""
Management script for OrgChar RAG system.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from orgchar.config import Config
from orgchar.rag_system import RAGSystem
from orgchar.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_knowledge_base(args):
    """Initialize the knowledge base from documents."""
    config = Config()
    config.ensure_directories()
    
    logger.info("Initializing knowledge base...")
    
    rag_system = RAGSystem(config)
    success = rag_system.load_knowledge_base(force_rebuild=True)
    
    if success:
        stats = rag_system.get_knowledge_base_stats()
        logger.info(f"Knowledge base initialized with {stats['document_count']} documents")
    else:
        logger.error("Failed to initialize knowledge base")
        sys.exit(1)

def update_knowledge_base(args):
    """Update the knowledge base with new documents."""
    config = Config()
    
    logger.info("Updating knowledge base...")
    
    rag_system = RAGSystem(config)
    success = rag_system.update_knowledge_base()
    
    if success:
        stats = rag_system.get_knowledge_base_stats()
        logger.info(f"Knowledge base updated with {stats['document_count']} documents")
    else:
        logger.error("Failed to update knowledge base")
        sys.exit(1)

def show_stats(args):
    """Show knowledge base statistics."""
    config = Config()
    
    rag_system = RAGSystem(config)
    loaded = rag_system.load_knowledge_base()
    
    if loaded:
        stats = rag_system.get_knowledge_base_stats()
        print("Knowledge Base Statistics:")
        print(f"  Status: {stats['status']}")
        print(f"  Document Count: {stats['document_count']}")
        print(f"  Embedding Model: {stats['embedding_model']}")
    else:
        print("Knowledge base not found or failed to load")

def run_streamlit(args):
    """Run the Streamlit web interface."""
    config = Config()
    config.ensure_directories()
    
    import subprocess
    
    app_path = Path(__file__).parent / "app.py"
    cmd = ["streamlit", "run", str(app_path)]
    
    if args.port:
        cmd.extend(["--server.port", str(args.port)])
    
    logger.info("Starting Streamlit application...")
    subprocess.run(cmd)

def run_discord_bot(args):
    """Run the Discord bot."""
    config = Config()
    config.ensure_directories()
    
    if not config.DISCORD_BOT_TOKEN:
        logger.error("Discord bot token not configured. Please set DISCORD_BOT_TOKEN in .env file.")
        sys.exit(1)
    
    from orgchar.discord_bot import run_discord_bot
    run_discord_bot(config)

def test_system(args):
    """Test the RAG system with a sample question."""
    config = Config()
    
    rag_system = RAGSystem(config)
    loaded = rag_system.load_knowledge_base()
    
    if not loaded:
        logger.error("Knowledge base not available. Run 'python manage.py init' first.")
        sys.exit(1)
    
    question = args.question or "What is organizational behavior?"
    
    logger.info(f"Testing with question: {question}")
    response = rag_system.answer_question(question)
    
    print("\n" + "="*50)
    print("QUESTION:", question)
    print("="*50)
    print("ANSWER:")
    print(response['answer'])
    
    if response['sources']:
        print("\nSOURCES:")
        for source in response['sources']:
            print(f"  - {source['filename']} ({source['type']})")
    
    print("="*50 + "\n")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="OrgChar RAG System Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize knowledge base')
    init_parser.set_defaults(func=init_knowledge_base)
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update knowledge base')
    update_parser.set_defaults(func=update_knowledge_base)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show knowledge base statistics')
    stats_parser.set_defaults(func=show_stats)
    
    # Web command
    web_parser = subparsers.add_parser('web', help='Run Streamlit web interface')
    web_parser.add_argument('--port', type=int, help='Port to run on')
    web_parser.set_defaults(func=run_streamlit)
    
    # Discord command
    discord_parser = subparsers.add_parser('discord', help='Run Discord bot')
    discord_parser.set_defaults(func=run_discord_bot)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test the system with a question')
    test_parser.add_argument('--question', '-q', help='Question to test with')
    test_parser.set_defaults(func=test_system)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()