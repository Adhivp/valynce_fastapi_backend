#!/bin/bash

# Valynce FastAPI Quick Start Script

echo "🚀 Starting Valynce FastAPI Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "valynce_venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv valynce_venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source valynce_venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual values!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔗 Aptos Endpoints: http://localhost:8000/aptos"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
