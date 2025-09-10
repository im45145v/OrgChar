#!/usr/bin/env python3
"""
Demo script showing OrgChar functionality without requiring API keys.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append('src')

from orgchar.document_processor import DocumentProcessor
from orgchar.config import Config

def main():
    print("🏢 OrgChar RAG Chatbot Demo")
    print("=" * 40)
    print()

    # Initialize config and ensure directories
    config = Config()
    config.ensure_directories()
    print("✅ Configuration initialized")

    # Process documents
    processor = DocumentProcessor(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    
    print(f"📚 Processing documents from: {config.KNOWLEDGE_BASE_PATH}")
    docs = processor.process_directory(config.KNOWLEDGE_BASE_PATH)
    print(f"✅ Processed {len(docs)} document chunks")
    print()

    # Show document sources
    sources = set(doc.metadata['filename'] for doc in docs)
    print("📂 Available knowledge sources:")
    for source in sorted(sources):
        source_docs = [doc for doc in docs if doc.metadata['filename'] == source]
        print(f"   • {source} ({len(source_docs)} chunks)")
    print()

    # Show sample content
    print("📖 Sample content:")
    for i, doc in enumerate(docs[:2], 1):
        print(f"{i}. From {doc.metadata['filename']}:")
        print(f"   {doc.page_content[:150]}...")
        print()

    # Simulate RAG functionality (without LLM)
    print("🔍 Simulated query processing:")
    query = "What are leadership styles?"
    print(f"Query: {query}")
    
    # Simple keyword matching simulation
    relevant_docs = []
    keywords = query.lower().split()
    
    for doc in docs:
        content_lower = doc.page_content.lower()
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > 0:
            relevant_docs.append((doc, score))
    
    # Sort by relevance score
    relevant_docs.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(relevant_docs)} relevant chunks:")
    for i, (doc, score) in enumerate(relevant_docs[:3], 1):
        print(f"{i}. {doc.metadata['filename']} (relevance: {score})")
        print(f"   Preview: {doc.page_content[:100]}...")
        print()

    print("🎯 System Status:")
    print("   ✅ Document processing: Working")
    print("   ✅ Knowledge base: Ready")
    print("   ✅ Similarity search: Simulated (requires embeddings)")
    print("   ⚠️  LLM responses: Requires OpenAI API key")
    print()
    print("🚀 To use full functionality:")
    print("   1. Set OPENAI_API_KEY in .env file")
    print("   2. Run: python manage.py init")
    print("   3. Run: python manage.py web")

if __name__ == "__main__":
    main()
