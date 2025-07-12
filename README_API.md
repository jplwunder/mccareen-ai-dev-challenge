# FastAPI Backend Setup

This directory contains a FastAPI backend for the Company Profile Generator application.

## Features

- **FastAPI** web framework with automatic API documentation
- **CORS middleware** for frontend integration
- **Pydantic models** for request/response validation
- **Virtual environment** for dependency isolation
- **Mock API endpoint** for website analysis

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Server

```bash
# Option 1: Use the start script
./start_api.sh

# Option 2: Run directly
source venv/bin/activate
python main.py

# Option 3: Use uvicorn directly
source venv/bin/activate
uvicorn api.src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API

```bash
# Run the test script
source venv/bin/activate
python test_api.py
```

## API Endpoints

- **GET /** - Root endpoint with API information
- **GET /health** - Health check endpoint
- **POST /api/analyze-website** - Analyze a website and generate company profile

### Example Request

```bash
curl -X POST "http://localhost:8000/api/analyze-website" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://example.com"}'
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── start_api.sh        # Start script
├── test_api.py         # API test script
├── venv/               # Virtual environment
└── README_API.md       # This file
```

## Development

### Adding New Endpoints

1. Define Pydantic models for request/response in `main.py`
2. Add the endpoint function with appropriate decorators
3. Test the endpoint using the test script or Swagger UI

### Environment Variables

You can create a `.env` file for environment-specific configuration:

```env
DEBUG=True
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key
```

## Deployment

For production deployment, consider:

- Using a production WSGI server like Gunicorn
- Setting up environment variables
- Adding authentication and authorization
- Implementing proper logging
- Adding a database for persistent storage

### Example Production Command

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
