import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq
from typing import List

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(
    title="Chatbot SMKN 4 Bojonegoro API",
    description="API Chatbot untuk Jurusan RPL SMKN 4 Bojonegoro",
    version="1.0.0"
)

# Tambahkan CORS agar bisa diakses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk production, ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint untuk health check (Render requirement)
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Chatbot SMKN 4 Bojonegoro API",
        "version": "1.0.0",
        "docs": "/docs"
    }



def load_all_documents(folder_path: str) -> List[str]:
    all_docs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".json") or filename.endswith(".txt") or filename.endswith(".docx"):
            loader = TextLoader(file_path)
            docs = loader.load()
            all_docs.extend(docs)
    return all_docs


documents = load_all_documents("data")
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings()
vectorstore = Chroma.from_documents(docs, embedding)
retriever = vectorstore.as_retriever()


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"  # Model terbaru yang masih supported
)

template = """
Kamu adalah chatbot resmi jurusan Rekayasa perangkat lunak SMKN 4 Bojonegoro, berbicara seolah menjawab langsung akan tetapi tanpa menyebut 'menurut data', buatlah cara bicaramu selayaknya manusia, sebaiknya jangan gunakan kata seperti "halo saya chatbot smkn 4 bojonegoro" disetiap pertanyaan, cukup ketika di tanya siapa kamu saja. Jawablah dengan jelas, profesional, dan sopan, dan yang paling penting gunakan bahasa indonesia.

{context}

Pertanyaan: {question}
Jawaban:
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_bot(query: Query):
    answer = qa_chain.run(query.question)
    return {"jawaban": answer}

