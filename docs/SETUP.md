# Setup Guide for OrgChar RAG Chatbot

This guide provides detailed setup instructions for the OrgChar organizational behavior RAG chatbot system.

## Prerequisites

- Python 3.8 or higher
- OpenAI API account and key
- Discord Developer Account (for Discord bot functionality)
- 4GB+ RAM recommended for vector operations

## Step-by-Step Setup

### 1. Environment Setup

#### Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv orgchar_env

# Activate virtual environment
# On Windows:
orgchar_env\Scripts\activate
# On macOS/Linux:
source orgchar_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### Alternative: Using conda

```bash
# Create conda environment
conda create -n orgchar python=3.9
conda activate orgchar

# Install requirements
pip install -r requirements.txt
```

### 2. API Configuration

#### OpenAI Setup

1. Visit [OpenAI API Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new secret key
5. Copy the key for configuration

#### Discord Bot Setup (Optional)

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Enable required intents:
   - Message Content Intent
   - Server Members Intent (optional)

### 3. Configuration

#### Create Environment File

```bash
cp .env.example .env
```

#### Configure .env File

```env
# Required: OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Discord Configuration
DISCORD_BOT_TOKEN=your-discord-bot-token-here
DISCORD_GUILD_ID=your-server-id-here

# Application Settings
KNOWLEDGE_BASE_PATH=./knowledge_base
VECTOR_DB_PATH=./vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. Directory Structure Setup

```bash
# Create required directories
mkdir knowledge_base
mkdir vector_db

# Set permissions (Linux/macOS)
chmod 755 knowledge_base vector_db
```

### 5. Document Preparation

#### Supported Formats

- PDF files (.pdf)
- Text files (.txt)
- Markdown files (.md)

#### Document Guidelines

1. **Quality**: Ensure documents are clear and well-formatted
2. **Relevance**: Focus on organizational behavior content
3. **Size**: Individual files should be under 50MB
4. **Language**: English content works best

#### Adding Documents

```bash
# Copy documents to knowledge base
cp /path/to/your/documents/* ./knowledge_base/

# Or create subdirectories for organization
mkdir knowledge_base/leadership
mkdir knowledge_base/culture  
mkdir knowledge_base/communication

# Example document structure
knowledge_base/
├── leadership/
│   ├── transformational_leadership.pdf
│   └── leadership_styles.txt
├── culture/
│   ├── organizational_culture.pdf
│   └── culture_change.md
└── communication/
    └── workplace_communication.pdf
```

### 6. Initial System Setup

#### Initialize Knowledge Base

```bash
# Process all documents and create vector index
python manage.py init
```

#### Verify Setup

```bash
# Check system status
python manage.py stats

# Test with sample question
python manage.py test --question "What is organizational behavior?"
```

### 7. Discord Bot Setup (Optional)

#### Bot Permissions

Required permissions for Discord bot:
- Send Messages
- Use Slash Commands
- Read Message History
- Embed Links
- Add Reactions

#### Invite Bot to Server

1. Go to Discord Developer Portal → Your Application → OAuth2 → URL Generator
2. Select "bot" and "applications.commands" scopes
3. Select required permissions
4. Use generated URL to invite bot to your server

#### Configure Bot

```bash
# Add bot token to .env file
DISCORD_BOT_TOKEN=your-bot-token-here
DISCORD_GUILD_ID=your-server-id-here
```

## Running the System

### Web Interface

```bash
# Run Streamlit web app
python manage.py web

# Or specify port
python manage.py web --port 8080

# Direct command
streamlit run app.py
```

Access at: `http://localhost:8501`

### Discord Bot

```bash
# Run Discord bot
python manage.py discord

# Or directly
python bot.py
```

### Both Services

```bash
# Terminal 1: Web interface
python manage.py web

# Terminal 2: Discord bot  
python manage.py discord
```

## Configuration Tuning

### Performance Settings

#### Chunk Size Optimization

```env
# For detailed responses (slower)
CHUNK_SIZE=1500
CHUNK_OVERLAP=300

# For faster responses (less context)
CHUNK_SIZE=800
CHUNK_OVERLAP=150
```

#### Model Selection

Edit `src/orgchar/config.py`:

```python
class Config:
    # Use different embedding model
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    
    # Use different LLM
    LLM_MODEL = "gpt-4"  # More accurate but slower
    # LLM_MODEL = "gpt-3.5-turbo"  # Faster and cheaper
```

### Memory Optimization

```python
# For systems with limited RAM
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Smaller model

# For better accuracy (requires more RAM)
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
```

## Security Best Practices

### API Key Protection

```bash
# Never commit .env file
echo ".env" >> .gitignore

# Use environment variables in production
export OPENAI_API_KEY="your-key-here"
```

### Discord Security

```bash
# Restrict bot permissions
# Use role-based access control
# Monitor bot usage logs
```

### File Security

```bash
# Set appropriate file permissions
chmod 600 .env
chmod 755 knowledge_base/
```

## Maintenance

### Regular Updates

```bash
# Update knowledge base with new documents
python manage.py update

# Rebuild entire knowledge base
python manage.py init
```

### Monitoring

```bash
# Check system status
python manage.py stats

# View logs
tail -f logs/orgchar.log
```

### Backup

```bash
# Backup knowledge base
tar -czf knowledge_base_backup.tar.gz knowledge_base/

# Backup vector database
tar -czf vector_db_backup.tar.gz vector_db/
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 2. OpenAI API Errors

```bash
# Check API key
python -c "import openai; print(openai.api_key)"

# Test API connection
python -c "
import openai
client = openai.OpenAI()
print(client.models.list())
"
```

#### 3. Vector Store Issues

```bash
# Clear and rebuild
rm -rf vector_db/
python manage.py init
```

#### 4. Discord Connection Issues

```bash
# Check bot token
# Verify bot permissions
# Check Discord API status
```

### Getting Help

- Check logs in console output
- Review error messages carefully
- Test individual components
- Consult Discord.py documentation for bot issues
- Check OpenAI API documentation for LLM issues

## Next Steps

After setup:

1. **Test thoroughly** with various questions
2. **Add more documents** to improve knowledge base
3. **Customize prompts** for your specific use case
4. **Monitor usage** and performance
5. **Train users** on effective question asking
6. **Set up monitoring** and logging for production use

## Production Deployment

For production deployment, consider:

- Use environment variables for all secrets
- Implement proper logging and monitoring
- Set up automated backups
- Use process managers (PM2, systemd)
- Configure reverse proxy (nginx) for web interface
- Implement rate limiting and security measures