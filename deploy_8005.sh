#!/bin/bash

# Check if docker-compose (v1) is available
if command -v docker-compose &> /dev/null
then
    echo "Using docker-compose (v1)..."
    docker-compose -f docker-compose-new.yml up --build -d
else
    # Fallback to docker compose (v2)
    echo "Using docker compose (v2)..."
    docker compose -f docker-compose-new.yml up --build -d
fi
