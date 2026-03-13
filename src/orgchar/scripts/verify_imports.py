#!/usr/bin/env python3
"""
Simple import verification script for current LangChain package usage.
Exit code 0 on success, non-zero on failure.
"""
import sys

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.documents import Document
    from langchain_openai import ChatOpenAI
    from sentence_transformers import SentenceTransformer
    from langchain_community.vectorstores import FAISS
except Exception as e:
    print("IMPORT-FAIL:", e, file=sys.stderr)
    sys.exit(2)

print("IMPORT-OK")
sys.exit(0)