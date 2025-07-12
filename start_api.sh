#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if we're in the virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
elif [ -f "api/requirements.txt" ]; then
    python -m pip install -r api/requirements.txt
else
    echo "❌ No requirements.txt found"
    exit 1
fi

# Export environment variables if .env exists
if [ -f ".env" ]; then
    echo "Loading environment variables from .env"
    export $(cat .env | xargs)
fi

# Start the FastAPI server
echo "🚀 Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"

# Check if main.py exists in the expected location
if [ -f "main.py" ]; then
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
elif [ -f "api/main.py" ]; then
    cd api && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
elif [ -f "api/src/main.py" ]; then
    uvicorn api.src.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "❌ Could not find main.py file"
    echo "Looking for main.py in:"
    echo "  - ./main.py"
    echo "  - ./api/main.py" 
    echo "  - ./api/src/main.py"
    exit 1
fi