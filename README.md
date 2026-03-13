# OrgChar - Organizational Behavior RAG Chatbot 🏢

A powerful Python-based RAG (Retrieval-Augmented Generation) chatbot system designed specifically for answering questions about organizational behavior, leadership, workplace dynamics, and management principles. The system uses local document knowledge bases and provides both web and Discord interfaces for easy access.

[![Watch the video](https://www.simplypsychology.org/wp-content/uploads/behavior-analysis.jpeg)](https://www.loom.com/share/c860c2b79a1146fc8d16cc0f443b1ea1?sid=ce2fdf92-b93e-4029-b478-88c585a29fcb)
## Features ✨

- **📚 Document Processing**: Automatically processes PDF, TXT, and Markdown documents
- **🔍 RAG System**: Advanced retrieval-augmented generation using vector embeddings
- **💻 Web Interface**: Clean Streamlit-based chat interface
- **🤖 Discord Bot**: Full-featured Discord integration with slash commands
- **⚡ Real-time Updates**: Easy knowledge base management and updates
- **📊 Analytics**: Built-in statistics and monitoring
- **🔧 Configurable**: Flexible configuration through environment variables

## Quick Start 🚀

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd OrgChar

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` file with your configurations:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Discord Bot Configuration (optional)
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here

# Application Configuration
KNOWLEDGE_BASE_PATH=./knowledge_base
VECTOR_DB_PATH=./vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Model Configuration
LLM_MODEL=gpt-4o-mini
TEMPERATURE=0.3
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Local fallback (recommended)
USE_LOCAL_FALLBACK=true
LOCAL_LLM_MODEL=google/flan-t5-base
LOCAL_MAX_NEW_TOKENS=512
```

### Streamlit Cloud Secrets (TOML)

For Streamlit Cloud deployments, set secrets in the app settings using TOML.
The app supports both flat keys and a namespaced `[orgchar]` section.

Flat format:

```toml
OPENAI_API_KEY = "your_openai_key"
DISCORD_BOT_TOKEN = "your_discord_token"
DISCORD_GUILD_ID = "your_guild_id"

KNOWLEDGE_BASE_PATH = "./knowledge_base"
VECTOR_DB_PATH = "./vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
USE_LOCAL_FALLBACK = true
LOCAL_LLM_MODEL = "google/flan-t5-base"
LOCAL_MAX_NEW_TOKENS = 512
```

Namespaced format:

```toml
[orgchar]
OPENAI_API_KEY = "your_openai_key"
DISCORD_BOT_TOKEN = "your_discord_token"
DISCORD_GUILD_ID = "your_guild_id"
KNOWLEDGE_BASE_PATH = "./knowledge_base"
VECTOR_DB_PATH = "./vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
USE_LOCAL_FALLBACK = true
LOCAL_LLM_MODEL = "google/flan-t5-base"
LOCAL_MAX_NEW_TOKENS = 512
```

### 3. Add Documents

Place your organizational behavior documents (PDF, TXT, MD) in the `knowledge_base` directory:

```bash
mkdir knowledge_base
# Copy your documents here
```

### 4. Initialize Knowledge Base

```bash
python manage.py init
```

### 5. Run the Application

**Demo Version (No API keys required):**
```bash
streamlit run app_offline.py
```

**Web Interface:**
```bash
python manage.py web
# or directly
streamlit run app.py
```

**Discord Bot:**
```bash
python manage.py discord
# or directly
python bot.py
```

### 6. Docker Deployment (Recommended for Production)

OrgChar can be easily deployed using Docker:

```bash
# Build and start all services
docker-compose up -d

# Run only the web interface
docker-compose up -d orgchar-web

# Run only the Discord bot
docker-compose up -d orgchar-discord

# Run the offline demo version (no OpenAI API required)
docker-compose up -d orgchar-offline

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

For custom configurations, edit the `.env` file before building the Docker containers.

## Usage Guide 📖

### Web Interface

1. **Chat Interface**: Ask questions directly in the chat
2. **Document Upload**: Upload new documents through the sidebar
3. **Knowledge Base Management**: Refresh and view statistics
4. **Settings**: Adjust retrieval parameters

### Discord Bot

**Commands:**
- `@OrgChar <question>` - Ask a question by mentioning the bot
- `!org ask <question>` - Ask a specific question
- `!org stats` - View knowledge base statistics  
- `!org orghelp` - Show help information
- `!org refresh` - Refresh knowledge base (Admin only)

**Example Questions:**
- "What is transformational leadership?"
- "How can we improve team collaboration?"
- "What are the key principles of organizational culture?"

### Management CLI

```bash
# Initialize or rebuild knowledge base
python manage.py init

# Update knowledge base with new documents
python manage.py update

# View statistics
python manage.py stats

# Test the system
python manage.py test --question "What is organizational behavior?"

# Run web interface on specific port
python manage.py web --port 8080

# Run Discord bot
python manage.py discord
```

## Architecture 🏗️

### Components

1. **Document Processor** (`document_processor.py`)
   - Handles PDF, TXT, and MD file processing
   - Text chunking with configurable overlap
   - Metadata extraction and management

2. **Vector Store** (`vector_store.py`)
   - FAISS-based vector storage
   - Sentence transformer embeddings
   - Similarity search and retrieval

3. **RAG System** (`rag_system.py`)
   - Core retrieval-augmented generation logic
   - OpenAI GPT integration
   - Context-aware response generation

4. **Streamlit App** (`streamlit_app.py`)
   - Web-based chat interface
   - Document upload and management
   - Real-time statistics and monitoring

5. **Discord Bot** (`discord_bot.py`)
   - Full Discord integration
   - Command handling and responses
   - Admin controls and permissions

### Data Flow

```
Documents → Document Processor → Vector Store → RAG System → User Interface
    ↓              ↓                   ↓            ↓           ↓
  PDF/TXT     Text Chunks        Embeddings    Responses   Web/Discord
```

## Configuration ⚙️

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | Required |
| `DISCORD_BOT_TOKEN` | Discord bot token | Optional |
| `DISCORD_GUILD_ID` | Discord guild ID | Optional |
| `KNOWLEDGE_BASE_PATH` | Path to documents directory | `./knowledge_base` |
| `VECTOR_DB_PATH` | Path to vector database | `./vector_db` |
| `CHUNK_SIZE` | Text chunk size for processing | `1000` |
| `CHUNK_OVERLAP` | Overlap between text chunks | `200` |

### Model Configuration

The system uses:
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: `gpt-4o-mini` (configurable)
- **Vector Store**: FAISS with cosine similarity
- **Fallback LLM**: `google/flan-t5-base` via Hugging Face pipeline

## Development 🛠️

### Project Structure

```
OrgChar/
├── src/orgchar/           # Main package
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── document_processor.py
│   ├── vector_store.py
│   ├── rag_system.py
│   ├── streamlit_app.py
│   └── discord_bot.py
├── knowledge_base/        # Document storage
├── vector_db/            # Vector database (auto-generated)
├── docs/                 # Additional documentation
├── app.py               # Streamlit entry point
├── bot.py               # Discord bot entry point
├── manage.py            # Management CLI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Adding New Features

1. **Custom Document Types**: Extend `DocumentProcessor` class
2. **New Vector Stores**: Implement new backends in `VectorStore`
3. **UI Enhancements**: Modify `StreamlitApp` class
4. **Bot Commands**: Add commands in `discord_bot.py`

## Troubleshooting 🔍

### Common Issues

1. **Knowledge Base Not Loading**
   ```bash
   python manage.py init  # Rebuild knowledge base
   ```

2. **OpenAI API Errors**
   - Verify API key in `.env` file
   - Check API quotas and billing

3. **Discord Bot Not Responding**
   - Verify bot token and permissions
   - Check bot is invited to server with correct permissions

4. **Document Processing Errors**
   - Ensure documents are in supported formats (PDF, TXT, MD)
   - Check file permissions and encoding

5. **Docker-related Issues**
   - **Container not starting**: Check logs with `docker-compose logs -f`
   - **Permission issues**: Make sure volumes have correct permissions
   - **Port conflicts**: Change port mappings in docker-compose.yml
   - **API keys not working**: Verify .env file is properly mounted
   - **Knowledge base empty**: Initialize manually with `docker-compose exec orgchar-web python manage.py init`

### Logs and Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

When using Docker, view logs with:
```bash
docker-compose logs -f [service-name]
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For questions, issues, or contributions:
- Open an issue on GitHub
- Join our Discord server
- Check the documentation in the `docs/` directory

---

Built with ❤️ using Python, Streamlit, LangChain, and Discord.py
