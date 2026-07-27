from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI(
    title="Job Offer Analyzer",
    description="Analyzes job offers based on your personal criteria",
    version="0.1.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)