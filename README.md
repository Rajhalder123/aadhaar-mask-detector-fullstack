<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=for-the-badge"/>
<img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

# 🛡️ Aadhaar Masking API

### AI-Powered Aadhaar Number Detection & Masking System

*Automatically detect and redact Aadhaar numbers from ID card images using YOLOv8 + OpenCV — protecting citizen privacy with one API call.*

</div>

---

## 📸 Demo

<div align="center">

| Input — Original Aadhaar Card | Output — Masked Card |
|:---:|:---:|
| <img src="assets/demo.png" width="280" alt="Before masking — full Aadhaar number visible"/> | *(Aadhaar digits redacted, last 4 visible)* |

> **Before:** Full 12-digit number exposed &nbsp;→&nbsp; **After:** First 8 digits masked, last 4 retained for reference

</div>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **AI Detection** | YOLOv8 model trained to locate Aadhaar number regions with high precision |
| 🎭 **Smart Masking** | OpenCV-based pixel redaction — keeps last 4 digits visible per UIDAI guidelines |
| ⚡ **Fast API** | FastAPI backend with async support — processes images in milliseconds |
| 🖼️ **Modern UI** | Glassmorphism frontend with drag-and-drop image upload |
| 📦 **REST API** | Clean JSON responses, easy to integrate into any pipeline |
| 🔒 **Privacy First** | Images processed locally — nothing stored permanently |

---

## 🗂️ Project Structure
```
aadhar-masking/
│
├── backend/                    # 🐍 FastAPI Server
│   ├── main.py                 # Application entry point & API routes
│   ├── MIXED_AADHAR...pt       # Trained YOLOv8 model weights
│   ├── uploads/                # Temporary input image storage
│   └── masked/                 # Processed output images
│
└── frontend/                   # 🌐 Web Interface
    ├── index.html              # Main UI (Glassmorphism design)
    └── assets/                 # CSS stylesheets & JS scripts
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/aadhar-masking.git
cd aadhar-masking
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

> **Key dependencies:** `fastapi`, `uvicorn`, `ultralytics`, `opencv-python`, `python-multipart`

### 3. Start the Backend API
```bash
cd backend
python -m uvicorn main:app --reload
```

✅ API is live at **`http://127.0.0.1:8000`**  
📖 Interactive docs at **`http://127.0.0.1:8000/docs`**

### 4. Start the Frontend
```bash
cd frontend
python -m http.server 3000
```

🌐 Visit **`http://localhost:3000`** in your browser.

---

## 🔌 API Reference

### `POST /mask`

Upload an Aadhaar card image and receive the masked version.

**Request**
```http
POST /mask
Content-Type: multipart/form-data

file: <image file>
```

**Response**
```json
{
  "status": "success",
  "masked_image_url": "/masked/output_xxxx.jpg",
  "detections": 1
}
```

---

## 🧠 How It Works
```
📤 Upload Image
      │
      ▼
🤖 YOLOv8 Model
   Detects bounding box
   around Aadhaar number
      │
      ▼
🎭 OpenCV Masking
   Fills detected region
   with black rectangle
   (preserves last 4 digits)
      │
      ▼
📥 Return Masked Image
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push and open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## ⚠️ Disclaimer

This tool is intended for **legitimate privacy-protection use cases** such as document redaction pipelines, KYC compliance, and data anonymization. Do not use it to tamper with or forge identity documents.

---

<div align="center">

Made with ❤️ for privacy &nbsp;|&nbsp; Powered by YOLOv8 + FastAPI

</div>
