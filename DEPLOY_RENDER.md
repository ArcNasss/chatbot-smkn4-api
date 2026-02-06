# 🚀 Deploy ke Render.com - Step by Step

## 📋 Checklist Sebelum Deploy:

✅ File `render.yaml` sudah ada  
✅ File `requirements.txt` sudah ada  
✅ File `.gitignore` sudah ada  
✅ API sudah tested di local  

---

## 🔧 STEP 1: Setup GitHub Repository

### 1.1 Initialize Git
```bash
git init
git add .
git commit -m "Initial commit - Chatbot SMKN 4 API"
```

### 1.2 Create GitHub Repository
1. Buka https://github.com/new
2. Repository name: `chatbot-smkn4` (atau nama lain)
3. **JANGAN** centang "Initialize with README" (sudah ada)
4. Visibility: **Public** atau **Private** (terserah)
5. Klik **"Create repository"**

### 1.3 Push ke GitHub
```bash
# Ganti <username> dengan GitHub username Anda
git remote add origin https://github.com/<username>/chatbot-smkn4.git
git branch -M main
git push -u origin main
```

**Akan muncul prompt login GitHub - masukkan kredensial Anda**

---

## 🚀 STEP 2: Deploy ke Render

### 2.1 Daftar/Login Render
1. Buka https://render.com
2. Klik **"Get Started"** atau **"Sign In"**
3. **Pilih "Sign in with GitHub"** (lebih mudah)
4. Authorize Render untuk akses GitHub

### 2.2 Create New Web Service
1. Dashboard Render → Klik **"New +"**
2. Pilih **"Web Service"**
3. Klik **"Connect account"** jika belum connect GitHub
4. **Cari repository** `chatbot-smkn4`
5. Klik **"Connect"**

### 2.3 Konfigurasi Service

Render akan auto-detect dari `render.yaml`, tapi pastikan:

| Field | Value |
|-------|-------|
| **Name** | chatbot-smkn4-api |
| **Region** | Singapore (terdekat) |
| **Branch** | main |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | **Free** ✅ |

### 2.4 Add Environment Variables

**PENTING!** Tambahkan GROQ API Key:

1. Scroll ke bawah ke **"Environment Variables"**
2. Klik **"Add Environment Variable"**
3. Key: `GROQ_API_KEY`
4. Value: `gsk_xxxxxxxxx` (paste API key Anda)
5. Klik **"Add"**

### 2.5 Deploy!

1. Klik **"Create Web Service"** di bawah
2. **Wait...** Render akan build & deploy (3-5 menit)
3. Lihat logs real-time

---

## ✅ STEP 3: Test API

### 3.1 Dapatkan URL
Setelah deploy sukses, Anda akan dapat URL seperti:
```
https://chatbot-smkn4-api.onrender.com
```

### 3.2 Test API
```bash
# Test via PowerShell
$body = @{
    question = "Apa saja jurusan di SMKN 4 Bojonegoro?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://chatbot-smkn4-api.onrender.com/ask" -Method Post -Body $body -ContentType "application/json"
```

### 3.3 Cek Swagger Docs
Buka di browser:
```
https://chatbot-smkn4-api.onrender.com/docs
```

---

## 🌐 STEP 4: Update Frontend

Update URL di `example_frontend.html`:

```javascript
// Ganti dari:
const API_URL = 'http://localhost:8000/ask';

// Jadi:
const API_URL = 'https://chatbot-smkn4-api.onrender.com/ask';
```

Upload frontend ke Netlify atau hosting lain.

---

## ⚠️ Catatan Penting:

### Cold Start
- Free tier Render akan "tidur" setelah 15 menit idle
- Request pertama butuh **20-30 detik** untuk "bangun"
- Request berikutnya normal cepat

### Solution Cold Start:
1. Gunakan **uptime monitoring** (gratis): UptimeRobot, Cron-job.org
2. Ping API setiap 14 menit untuk keep alive
3. Atau upgrade ke paid plan ($7/mo) - no cold start

---

## 🔄 Update Code Nanti:

```bash
# Edit code
git add .
git commit -m "Update feature"
git push

# Render akan AUTO-DEPLOY! 🎉
```

---

## 📊 Monitoring

**Render Dashboard:**
- Logs real-time
- Metrics (CPU, Memory)
- Deploy history
- Environment variables

---

## 🆘 Troubleshooting

### Build Failed?
- Cek logs di Render dashboard
- Pastikan `requirements.txt` lengkap
- Pastikan Python version compatible

### Health Check Failed?
- Render butuh root endpoint `/`
- Tambahkan di `main.py` jika perlu

### Environment Variable Error?
- Double check `GROQ_API_KEY` sudah diset
- Restart service

---

## 💰 Cost

**100% GRATIS** ✅
- Free tier: 750 hours/month
- Auto-sleep after 15 min idle
- Unlimited projects

Cukup untuk chatbot sekolah!

---

Selamat! API Anda sudah live di internet! 🎉
