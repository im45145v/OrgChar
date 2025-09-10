# OrgChar API Documentation

This document provides comprehensive API documentation for the OrgChar RAG system components.

## Core Classes

### Config

Configuration management for the OrgChar system.

```python
from orgchar.config import Config

config = Config()
config.ensure_directories()
```

#### Properties

- `OPENAI_API_KEY`: OpenAI API key
- `DISCORD_BOT_TOKEN`: Discord bot token  
- `KNOWLEDGE_BASE_PATH`: Path to documents
- `VECTOR_DB_PATH`: Path to vector database
- `CHUNK_SIZE`: Text chunk size (default: 1000)
- `CHUNK_OVERLAP`: Chunk overlap (default: 200)
- `EMBEDDING_MODEL`: Embedding model name
- `LLM_MODEL`: Language model name

#### Methods

- `ensure_directories()`: Create required directories

### DocumentProcessor

Handles document loading and processing.

```python
from orgchar.document_processor import DocumentProcessor

processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
```

#### Methods

##### `load_pdf(file_path: Path) -> str`

Load text from PDF file.

**Parameters:**
- `file_path`: Path to PDF file

**Returns:**
- Extracted text content

**Example:**
```python
from pathlib import Path
text = processor.load_pdf(Path("document.pdf"))
```

##### `load_text_file(file_path: Path) -> str`

Load text from text file.

**Parameters:**
- `file_path`: Path to text file

**Returns:**
- File content as string

##### `load_documents_from_directory(directory_path: Path) -> List[Document]`

Load all supported documents from directory.

**Parameters:**
- `directory_path`: Path to document directory

**Returns:**
- List of processed Document objects

**Example:**
```python
from pathlib import Path
documents = processor.load_documents_from_directory(Path("./knowledge_base"))
```

##### `chunk_documents(documents: List[Document]) -> List[Document]`

Split documents into chunks.

**Parameters:**
- `documents`: List of documents to chunk

**Returns:**
- List of chunked documents

##### `process_directory(directory_path: Path) -> List[Document]`

Complete processing pipeline.

**Parameters:**
- `directory_path`: Path to document directory

**Returns:**
- List of processed and chunked documents

### VectorStore

Manages document embeddings and similarity search.

```python
from orgchar.vector_store import VectorStore

vector_store = VectorStore(embedding_model="sentence-transformers/all-MiniLM-L6-v2")
```

#### Methods

##### `create_index(documents: List[Document]) -> None`

Create vector index from documents.

**Parameters:**
- `documents`: List of documents to index

**Example:**
```python
vector_store.create_index(documents)
```

##### `add_documents(documents: List[Document]) -> None`

Add documents to existing index.

**Parameters:**
- `documents`: List of documents to add

##### `similarity_search(query: str, k: int = 4) -> List[Document]`

Perform similarity search.

**Parameters:**
- `query`: Search query
- `k`: Number of results to return

**Returns:**
- List of similar documents

**Example:**
```python
results = vector_store.similarity_search("leadership styles", k=5)
```

##### `similarity_search_with_score(query: str, k: int = 4) -> List[Tuple[Document, float]]`

Similarity search with scores.

**Parameters:**
- `query`: Search query
- `k`: Number of results to return

**Returns:**
- List of tuples (document, similarity_score)

##### `save_index(file_path: Path) -> None`

Save vector store to disk.

**Parameters:**
- `file_path`: Path to save location

##### `load_index(file_path: Path) -> bool`

Load vector store from disk.

**Parameters:**
- `file_path`: Path to load from

**Returns:**
- True if loaded successfully

##### `get_stats() -> dict`

Get vector store statistics.

**Returns:**
- Dictionary with status and document count

### RAGSystem

Main RAG system for question answering.

```python
from orgchar.rag_system import RAGSystem
from orgchar.config import Config

config = Config()
rag = RAGSystem(config)
```

#### Methods

##### `load_knowledge_base(force_rebuild: bool = False) -> bool`

Load or rebuild knowledge base.

**Parameters:**
- `force_rebuild`: Whether to force rebuilding

**Returns:**
- True if successful

**Example:**
```python
success = rag.load_knowledge_base()
```

##### `add_documents_to_knowledge_base(documents: List[Document]) -> bool`

Add documents to knowledge base.

**Parameters:**
- `documents`: List of documents to add

**Returns:**
- True if successful

##### `retrieve_context(query: str, k: int = 4) -> List[Document]`

Retrieve relevant context.

**Parameters:**
- `query`: User query
- `k`: Number of documents to retrieve

**Returns:**
- List of relevant documents

##### `generate_answer(question: str, context_docs: List[Document]) -> str`

Generate answer using LLM.

**Parameters:**
- `question`: User question
- `context_docs`: Retrieved context documents

**Returns:**
- Generated answer

##### `answer_question(question: str, retrieve_k: int = 4) -> Dict[str, Any]`

Complete RAG pipeline.

**Parameters:**
- `question`: User question
- `retrieve_k`: Number of context documents

**Returns:**
- Dictionary containing answer and metadata

**Example:**
```python
response = rag.answer_question("What is transformational leadership?")
print(response['answer'])
print(response['sources'])
```

##### `get_knowledge_base_stats() -> Dict[str, Any]`

Get knowledge base statistics.

**Returns:**
- Dictionary with statistics

##### `update_knowledge_base() -> bool`

Update knowledge base.

**Returns:**
- True if successful

## Response Formats

### Answer Response

The `answer_question` method returns a dictionary with:

```python
{
    'answer': str,           # Generated answer
    'sources': List[dict],   # Source documents used
    'context_count': int,    # Number of context docs
    'question': str          # Original question
}
```

### Source Format

Each source in the sources list contains:

```python
{
    'filename': str,    # Document filename
    'type': str,        # Document type (PDF, TXT, MD)
    'chunk_id': int     # Chunk identifier
}
```

### Statistics Format

Knowledge base statistics:

```python
{
    'status': str,           # 'initialized' or 'not_initialized'
    'document_count': int,   # Number of indexed documents
    'embedding_model': str   # Embedding model used
}
```

## Usage Examples

### Basic RAG Pipeline

```python
from pathlib import Path
from orgchar.config import Config
from orgchar.rag_system import RAGSystem

# Setup
config = Config()
config.ensure_directories()

# Initialize RAG system
rag = RAGSystem(config)

# Load knowledge base
success = rag.load_knowledge_base()
if not success:
    print("Failed to load knowledge base")
    exit(1)

# Ask question
response = rag.answer_question("What are the key leadership styles?")

print("Answer:", response['answer'])
print("Sources:", [s['filename'] for s in response['sources']])
```

### Document Processing

```python
from pathlib import Path
from orgchar.document_processor import DocumentProcessor

# Process documents
processor = DocumentProcessor(chunk_size=800, chunk_overlap=150)
documents = processor.process_directory(Path("./my_docs"))

print(f"Processed {len(documents)} document chunks")
```

### Vector Store Operations

```python
from orgchar.vector_store import VectorStore
from pathlib import Path

# Initialize vector store
vector_store = VectorStore()

# Create index
vector_store.create_index(documents)

# Save to disk
vector_store.save_index(Path("./my_vector_db"))

# Search
results = vector_store.similarity_search("team collaboration", k=3)
for doc in results:
    print(doc.page_content[:100])
```

### Custom Configuration

```python
from orgchar.config import Config
import os

# Custom configuration
class MyConfig(Config):
    def __init__(self):
        super().__init__()
        self.CHUNK_SIZE = 1200
        self.CHUNK_OVERLAP = 250
        self.LLM_MODEL = "gpt-4"
        self.TEMPERATURE = 0.5

# Use custom config
config = MyConfig()
rag = RAGSystem(config)
```

## Error Handling

### Common Exceptions

```python
try:
    rag = RAGSystem()
    rag.load_knowledge_base()
    response = rag.answer_question("test question")
except FileNotFoundError:
    print("Knowledge base files not found")
except ValueError:
    print("Invalid configuration")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Validation

```python
# Check if system is ready
stats = rag.get_knowledge_base_stats()
if stats['status'] != 'initialized':
    print("System not ready")
    
# Validate question
if not question or len(question.strip()) < 3:
    print("Question too short")
```

## Integration Examples

### Flask API

```python
from flask import Flask, request, jsonify
from orgchar.rag_system import RAGSystem

app = Flask(__name__)
rag = RAGSystem()
rag.load_knowledge_base()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    response = rag.answer_question(question)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orgchar.rag_system import RAGSystem

app = FastAPI()
rag = RAGSystem()

class QuestionRequest(BaseModel):
    question: str
    retrieve_k: int = 4

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        response = rag.answer_question(
            request.question, 
            retrieve_k=request.retrieve_k
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Best Practices

1. **Initialize Once**: Create RAG system instance once and reuse
2. **Error Handling**: Always handle potential exceptions
3. **Validation**: Validate inputs before processing
4. **Logging**: Use logging for debugging and monitoring
5. **Resource Management**: Properly manage memory for large document sets
6. **Caching**: Consider caching frequent queries
7. **Monitoring**: Track performance and usage metrics