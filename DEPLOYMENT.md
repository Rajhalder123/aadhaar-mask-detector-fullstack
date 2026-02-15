# Deployment Guide 🚀

To take this project from local to production, follow these steps for the Backend and Frontend.

## 1. Backend Deployment (FastAPI)

Recommended Platforms: **Render**, **Railway**, or **Railway**.

### Steps for [Render.com](https://render.com):
1. Create a new **Web Service**.
2. Connect your GitHub repository.
3. **Environment**: Python
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Root Directory**: `backend`
7. Add Environment Variable: `PYTHON_VERSION` = `3.9` (or your version).

> [!NOTE]
> Render's free tier spins down after inactivity. The first request after a break might take 30-60 seconds.

---

## 2. Frontend Deployment (Static Site)

Recommended Platforms: **Vercel**, **Netlify**, or **GitHub Pages**.

### CRITICAL: Update API URL
Before deploying the frontend, you **must** update the `API_URL` in `frontend/assets/js/script.js` to your production backend URL.

```javascript
// Change this:
const API_URL = 'http://127.0.0.1:8000/mask/';

// To this (example):
const API_URL = 'https://your-backend-name.onrender.com/mask/';
```

### Steps for [Vercel](https://vercel.com):
1. Push your code to GitHub.
2. Import the project into Vercel.
3. Set **Root Directory** to `frontend`.
4. Deploy!

---

## 3. Production Checklist

- [ ] **CORS**: Update `allow_origins` in `backend/main.py` to your specific frontend URL.
- [ ] **Dependencies**: Ensure `requirements.txt` is updated.
- [ ] **Model File**: Ensure `MIXED_AADHAR_NO_DETECT.pt` is uploaded with your code.
- [ ] **HTTPS**: Both frontend and backend should use HTTPS to avoid "Mixed Content" errors.

---

## Using Docker (Alternative)
If you prefer Docker, you can use a `Dockerfile` in the `backend/` directory:

```dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```
