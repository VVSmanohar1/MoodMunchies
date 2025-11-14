#!/bin/bash
# Script to start the Python ML API server

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the server
python -m uvicorn api.main:app --reload --port 8000

