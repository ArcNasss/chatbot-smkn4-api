# 🚀 Deploy ke Railway - GRATIS Tanpa Kartu Kredit

## ✅ Keuntungan Railway:

- **NO credit card needed** untuk start
- Login pakai GitHub saja
- $5 credit gratis/bulan (cukup untuk API ini)
- Deploy cepat (5-10 menit)
- No cold start
- Auto HTTPS & SSL

---

## 📋 Langkah Deploy (Super Mudah):

### **Opsi 1: Via Web (Paling Mudah)** ⭐

1. **Buka https://railway.app**

2. **Klik "Start a New Project"**

3. **Login with GitHub** (no registration needed)

4. **Deploy from GitHub Repo:**
   - Pilih "Deploy from GitHub repo"
   - Cari repository `chatbot-smkn4-api`
   - Klik repository tersebut

5. **Add Environment Variable:**
   - Klik tab "Variables"
   - Klik "New Variable"
   - Name: `GROQ_API_KEY`
   - Value: `<your-groq-api-key>` (paste API key Anda dari file .env)
   - Klik "Add"

6. **Done!** Railway auto-detect Python & deploy

7. **Ambil URL:**
   - Klik tab "Settings"
   - Scroll ke "Domains"
   - Klik "Generate Domain"
   - Copy URL: `https://your-app.up.railway.app`

---

### **Opsi 2: Via CLI**

```bash
# Install Railway CLI (jika belum punya Node.js, skip ke Opsi 1)
npm install -g railway

# Login (akan buka browser untuk login GitHub)
railway login

# Di folder project
cd C:\vscode\chatbot-smkn4

# Initialize Railway project
railway init

# Deploy
railway up

# Add environment variable (ganti dengan API key Anda)
railway variables set GROQ_API_KEY=your_groq_api_key_here

# Generate public URL
railway domain
```

---

## 🎯 Troubleshooting:

### Error: "No package.json found"
✅ **Ignore** - Railway akan auto-detect Python dari `requirements.txt`

### Error: "Start command not found"
Railway biasanya auto-detect, tapi kalau tidak:
1. Buka Railway dashboard
2. Settings → Start Command
3. Isi: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 📊 Monitoring:

Setelah deploy:
- **Logs**: Real-time di dashboard
- **Metrics**: CPU, Memory, Network usage
- **URL**: https://your-project.up.railway.app

---

## 💰 Free Tier Info:

- **$5 credit** setiap bulan (reset otomatis)
- Usage API ini: ~$2-3/bulan
- **Tidak perlu kartu kredit** untuk mulai
- Kalau mau extend limit: baru perlu kartu (optional)

---

## ✅ Setelah Deploy Berhasil:

Test API:
```
https://your-project.up.railway.app/docs
```

Update frontend:
```javascript
// Di example_frontend.html
const API_URL = 'https://your-project.up.railway.app/ask';
```

---

## 🔄 Auto Deploy:

Setiap push ke GitHub, Railway otomatis deploy ulang! 🎉

```bash
# Edit code
git add .
git commit -m "Update feature"
git push

# Railway auto-deploy! ✅
```
