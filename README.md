# Chatbot SMKN 4 Bojonegoro - API

API Chatbot untuk Jurusan RPL SMKN 4 Bojonegoro menggunakan FastAPI, LangChain, dan Groq.

## 🚀 Features

- RAG-based chatbot dengan vector database
- FastAPI REST API
- CORS enabled untuk frontend integration
- Real-time responses menggunakan Groq LLM

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **LangChain** - LLM orchestration
- **ChromaDB** - Vector database
- **Groq** - LLM provider (Llama 3.3)
- **HuggingFace** - Embeddings

## 📦 Installation

```bash
# Clone repository
git clone <your-repo-url>

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
# Buat file .env dan tambahkan:
GROQ_API_KEY=your_groq_api_key_here
```

## 🔧 Usage

### Local Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server akan berjalan di: http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoint

**POST** `/ask`

Request:
```json
{
  "question": "Apa saja jurusan di SMKN 4 Bojonegoro?"
}
```

Response:
```json
{
  "jawaban": "SMKN 4 Bojonegoro memiliki 6 jurusan: Rekayasa Perangkat Lunak, Kuliner, Teknik Pengelasan, Geologi Pertambangan, Perhotelan, dan Agribisnis Ternak Ruminansia."
}
```

## 🌐 Frontend Integration

Lihat file `example_frontend.html` untuk contoh implementasi frontend.

## 🚀 Deployment

### Railway

```bash
railway login
railway init
railway up
railway variables set GROQ_API_KEY=your_key_here
```

### Render

Push ke GitHub, lalu deploy via Render dashboard.

## 📁 Project Structure

```
chatbot-smkn4/
├── main.py                  # FastAPI application
├── data/
│   └── info_sekolah.json   # Knowledge base
├── requirements.txt         # Dependencies
├── railway.json            # Railway config
├── render.yaml             # Render config
├── example_frontend.html   # Frontend example
└── README.md
```

## 📄 License

MIT

## 👨‍💻 Author

SMKN 4 Bojonegoro - Jurusan RPL
