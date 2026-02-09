import os
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(title="Chatbot SMKN 4 Bojonegoro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load school data
data_file = Path(__file__).parent / "data" / "info_sekolah.json"
with open(data_file, "r", encoding="utf-8") as f:
    school_data = json.load(f)

# Convert to text context
context_text = json.dumps(school_data, indent=2, ensure_ascii=False)

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
    
)

template = """
Kamu adalah chatbot resmi jurusan Rekayasa perangkat lunak SMKN 4 Bojonegoro, berbicara seolah menjawab langsung akan tetapi tanpa menyebut 'menurut data', buatlah cara bicaramu selayaknya manusia, sebaiknya jangan gunakan kata seperti "halo saya chatbot smkn 4 bojonegoro" disetiap pertanyaan, cukup ketika di tanya siapa kamu saja. Jawablah dengan jelas, profesional, dan sopan, dan yang paling penting gunakan bahasa indonesia.

Data Sekolah:
{context}

Pertanyaan: {question}
Jawaban:
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

class Query(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {
        "message": "Chatbot SMKN 4 Bojonegoro API",
        "status": "online",
        "version": "1.0"
    }

@app.post("/ask")
def ask_bot(query: Query):
    try:
        full_prompt = prompt.format(context=context_text, question=query.question)
        response = llm.invoke(full_prompt)
        return {"jawaban": response.content}
    except Exception as e:
        error_message = str(e)
        
        # Handle rate limit errors specifically
        if "rate_limit_exceeded" in error_message.lower() or "429" in error_message:
            return {
                "jawaban": "Maaf, batas penggunaan API telah tercapai. Silakan coba lagi nanti atau hubungi administrator.",
                "error": "rate_limit_exceeded"
            }
        
        # Handle other errors
        return {
            "jawaban": "Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Silakan coba lagi.",
            "error": "internal_error"
        }

# For Vercel serverless
app = app

