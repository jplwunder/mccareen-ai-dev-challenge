# McCarren AI Development Challenge

An AI-powered company profile generator that analyzes websites and extracts key business information using Google's Gemini AI.

## Prerequisites

- **Node.js** 20.18.0+ (for frontend)
- **Python** 3.13+ (for backend)
- **Google Gemini API Key** (for AI analysis)

## Running

### 1. Clone and Setup

```bash
git clone <repository-url>
cd mccarren-ai-dev-challenge
```

### 2. Backend Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r api/requirements.txt
```

### 3. Environment Configuration

```bash
# Edit .env file and add your API key
GEMINI_API_KEY=your_actual_api_key_here

# Optional
VITE_API_URL=http://localhost:8000
```

### 4. Start Backend

```bash
./start_api.sh
# Backend runs on http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 5. Start Frontend

```bash
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

## API Documentation

### Main Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /api/analyze-website` - Analyze website and generate company profile

### Example Request

```bash
curl -X POST "http://localhost:8000/api/analyze-website?website_url=https://openai.com"
```

### Example Response

```json
{
  "company_name": "OpenAI",
  "service_lines": ["Artificial Intelligence", "Machine Learning", "API Services"],
  "company_description": "OpenAI is an AI research and deployment company...",
  "tier1_keywords": ["artificial intelligence", "machine learning", "AI"],
  "tier2_keywords": ["neural networks", "deep learning", "automation"],
  "emails": ["contact@openai.com"],
  "point_of_contact": "Support Team"
}
```
