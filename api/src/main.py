from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))

from api.src.presentation import router as presentation_router

# Create FastAPI instance
app = FastAPI(
    title="Company Profile Generator API",
    description="API for analyzing company websites and generating business profiles",
    version="1.0.0",
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "https://mccareen-ai-dev-challenge.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(presentation_router, prefix="/api", tags=["presentation"])


# Serve static files (for production)
if os.path.exists("dist"):
    app.mount("/static", StaticFiles(directory="dist"), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA for any unmatched routes"""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")

        file_path = f"dist/{full_path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        else:
            return FileResponse("dist/index.html")


if __name__ == "__main__":
    uvicorn.run(
        "api.src.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
