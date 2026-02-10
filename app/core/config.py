"""
Configuration file untuk chatbot
Menyimpan semua konfigurasi aplikasi di satu tempat
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM Configuration - Model hemat token
LLM_MODEL = "llama-3.1-8b-instant"  # Model yang lebih cepat dan hemat token
LLM_TEMPERATURE = 0.3  # Rendah untuk jawaban lebih konsisten
LLM_MAX_TOKENS = 150  # Batasi output agar hemat token

# Cache Configuration
CACHE_ENABLED = True
CACHE_TTL = 3600  # Time to live: 1 jam (dalam detik)

# Retrieval Configuration
MAX_CONTEXT_LENGTH = 500  # Maksimal karakter context yang dikirim ke LLM
SIMILARITY_THRESHOLD = 0.6  # Threshold untuk menentukan relevansi

# Prompt Template - Ringkas dan efisien
SYSTEM_PROMPT = "Kamu asisten jurusan RPL SMKN 4 Bojonegoro. Jawab singkat dan jelas berdasarkan data."
