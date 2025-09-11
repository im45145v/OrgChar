#!/bin/bash
# Script to build and save Docker images for offline installation on Raspberry Pi

echo "Building OrgChar Docker images for offline installation..."

# Create output directory
mkdir -p docker-images

# Build the images
docker compose build

# Save images to tar files
echo "Saving images to tar files..."
docker save orgchar-web:latest -o docker-images/orgchar-web.tar
docker save orgchar-discord:latest -o docker-images/orgchar-discord.tar

echo "Creating deployment package..."
# Create a deployment package
tar -czf orgchar-deployment.tar.gz \
    docker-images/ \
    docker-compose.yml \
    docker-helper.sh \
    knowledge_base/ \
    .env.example \
    README.md

echo "Done! Transfer orgchar-deployment.tar.gz to your Raspberry Pi."
echo ""
echo "Instructions for Raspberry Pi:"
echo "1. Extract the package: tar -xzf orgchar-deployment.tar.gz"
echo "2. Load the Docker images:"
echo "   docker load -i docker-images/orgchar-web.tar"
echo "   docker load -i docker-images/orgchar-discord.tar"
echo "3. Create .env file: cp .env.example .env"
echo "4. Edit .env file with your configuration"
echo "5. Start the services: docker compose up -d"
