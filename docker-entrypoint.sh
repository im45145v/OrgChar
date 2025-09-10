#!/bin/bash
set -e

# Function to initialize the knowledge base
init_knowledge_base() {
  echo "Initializing knowledge base..."
  python manage.py init
}

# Main logic based on command
case "$1" in
  web)
    init_knowledge_base
    echo "Starting web interface..."
    exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0
    ;;
  discord)
    init_knowledge_base
    echo "Starting Discord bot..."
    exec python manage.py discord
    ;;
  offline)
    echo "Starting offline demo mode..."
    exec streamlit run app_offline.py --server.port=8501 --server.address=0.0.0.0
    ;;
  init)
    init_knowledge_base
    ;;
  *)
    echo "Unknown command: $1"
    echo "Available commands: web, discord, offline, init"
    exit 1
    ;;
esac
