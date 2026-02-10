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
LLM_TEMPERATURE = 0.5  # Sedikit lebih tinggi untuk jawaban lebih natural
LLM_MAX_TOKENS = 200  # Cukup untuk penjelasan informatif

# Cache Configuration
CACHE_ENABLED = True
CACHE_TTL = 3600  # Time to live: 1 jam (dalam detik)

# Retrieval Configuration
MAX_CONTEXT_LENGTH = 500  # Maksimal karakter context yang dikirim ke LLM
SIMILARITY_THRESHOLD = 0.6  # Threshold untuk menentukan relevansi

# Prompt Template - Natural dan informatif
SYSTEM_PROMPT = """Kamu chatbot SMKN 4 Bojonegoro yang membantu siswa dengan ramah dan informatif.

Aturan:
- Jawab dengan bahasa natural seperti manusia
- Jika ada di data, jelaskan berdasarkan data
- Jika tidak ada di data tapi relevan, jelaskan dengan pengetahuan umum
- Format: definisi singkat + penjelasan jika perlu
- Jangan bilang "tidak tahu" jika bisa dijelaskan
- Ringkas tapi informatif"""
