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
    exec python manage.py web
    ;;
  discord)
    init_knowledge_base
    echo "Starting Discord bot..."
    exec python manage.py discord
    ;;
  offline)
    echo "Starting offline demo mode..."
    exec python manage.py offline
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
