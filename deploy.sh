#!/bin/bash

echo "Building and starting NutriTracker..."

# Build and start services
docker-compose up --build -d

echo "Services started!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Database: localhost:5432"

# Show running containers
docker-compose ps
