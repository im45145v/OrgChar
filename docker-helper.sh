#!/bin/bash
# Docker helper script for OrgChar

show_help() {
  echo "OrgChar Docker Helper"
  echo "Usage: ./docker-helper.sh [command]"
  echo ""
  echo "Commands:"
  echo "  start-web      - Start the web interface"
  echo "  start-discord  - Start the Discord bot"
  echo "  start-offline  - Start the offline demo"
  echo "  start-all      - Start all services"
  echo "  stop           - Stop all services"
  echo "  logs [service] - View logs (optional: specify service)"
  echo "  rebuild        - Rebuild containers"
  echo "  init-kb        - Initialize knowledge base"
  echo "  status         - Check status of containers"
  echo "  help           - Show this help message"
  echo ""
  echo "Examples:"
  echo "  ./docker-helper.sh start-web"
  echo "  ./docker-helper.sh logs orgchar-discord"
}

case "$1" in
  start-web)
    docker-compose up -d orgchar-web
    echo "Web interface started at http://localhost:8501"
    ;;
  start-discord)
    docker-compose up -d orgchar-discord
    echo "Discord bot started"
    ;;
  start-offline)
    # Uncomment the offline service in docker-compose.yml first
    sed -i 's/#orgchar-offline/orgchar-offline/g' docker-compose.yml
    docker-compose up -d orgchar-offline
    echo "Offline demo started at http://localhost:8502"
    ;;
  start-all)
    docker-compose up -d
    echo "All services started"
    ;;
  stop)
    docker-compose down
    echo "All services stopped"
    ;;
  logs)
    if [ -z "$2" ]; then
      docker-compose logs -f
    else
      docker-compose logs -f "$2"
    fi
    ;;
  rebuild)
    docker-compose build
    echo "Containers rebuilt"
    ;;
  init-kb)
    docker-compose exec orgchar-web python manage.py init
    echo "Knowledge base initialized"
    ;;
  status)
    docker-compose ps
    ;;
  help|*)
    show_help
    ;;
esac
