#!/bin/bash
# ================================================
# Production Start Script for YouTube Backend
# ================================================

echo "🚀 Starting YouTube Tools Backend..."

# Go to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start FastAPI
PYTHONPATH=src uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info