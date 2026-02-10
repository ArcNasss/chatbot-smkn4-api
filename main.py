"""
Main FastAPI Application
Endpoint chatbot SMKN 4 Bojonegoro dengan arsitektur hemat token
Architecture: Clean, modular, dan enterprise-ready
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.answer_service import answer_service
from app.services.cache_service import cache_service

# Initialize FastAPI app
app = FastAPI(
    title="Chatbot SMKN 4 Bojonegoro API",
    description="API chatbot dengan arsitektur hemat token menggunakan hybrid answer system",
    version="2.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    question: str

# Response model untuk dokumentasi yang lebih baik
class AnswerResponse(BaseModel):
    jawaban: str
    source: str = "llm"
    metadata: dict = {}

@app.get("/")
def read_root():
    """
    Health check endpoint
    """
    return {
        "message": "Chatbot SMKN 4 Bojonegoro API",
        "status": "online",
        "version": "2.0",
        "architecture": "hybrid-answer-system",
        "features": [
            "Direct answer (no LLM)",
            "Smart caching",
            "Relevant data retrieval",
            "Token-efficient LLM calls"
        ]
    }

@app.post("/ask", response_model=AnswerResponse)
def ask_bot(query: Query):
    """
    Main endpoint untuk bertanya
    
    Flow:
    1. Coba direct answer (tanpa LLM) - HEMAT TOKEN
    2. Check cache - HEMAT TOKEN
    3. Retrieve relevant data only - HEMAT TOKEN
    4. Call LLM with minimal context - TOKEN EFFICIENT
    
    Returns:
    - jawaban: Jawaban dari sistem
    - source: "direct" | "cache" | "llm" | "fallback"
    - metadata: Informasi tambahan tentang proses
    """
    result = answer_service.get_answer(query.question)
    return result

@app.get("/stats")
def get_stats():
    """
    Endpoint untuk melihat statistik penggunaan
    Berguna untuk monitoring efisiensi token
    """
    return {
        "answer_service": answer_service.get_stats(),
        "cache_service": cache_service.stats()
    }

@app.post("/cache/clear")
def clear_cache():
    """
    Endpoint untuk membersihkan cache (admin only in production)
    """
    cache_service.clear()
    return {"message": "Cache cleared successfully"}

@app.post("/stats/reset")
def reset_stats():
    """
    Reset statistik answer service (admin only in production)
    """
    answer_service.reset_stats()
    return {"message": "Statistics reset successfully"}

# For Vercel serverless compatibility
app = app

