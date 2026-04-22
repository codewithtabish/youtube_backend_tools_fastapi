#!/bin/bash
echo "🚀 Starting YouTube Tools Backend on EC2..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    exit 1
fi

echo "✅ Virtual environment activated"

# Run with Gunicorn + Uvicorn (Best for production)
exec gunicorn src.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --bind 0.0.0.0:${PORT:-8000} \
    --log-level info \
    --access-logfile - \
    --error-logfile -