"""
LLM initialization module
Menginisialisasi Groq LLM dengan konfigurasi hemat token
"""
from langchain_groq import ChatGroq
from app.core.config import (
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS
)

def get_llm():
    """
    Mengembalikan instance LLM yang sudah dikonfigurasi
    Menggunakan model hemat token dengan parameter optimal
    """
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        timeout=10,  # Timeout 10 detik
        max_retries=2  # Retry maksimal 2 kali
    )

# Instance LLM global yang bisa digunakan di seluruh aplikasi
llm = get_llm()
