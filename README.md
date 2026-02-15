# Aadhaar Masking Project

This project provides an AI-powered API to detect and mask Aadhaar numbers on ID cards, along with a modern web frontend.

## Project Structure

```
/aadhar-project
├── /backend                 # FastAPI Server & YOLO Model
│   ├── main.py              # Application Entry Point
│   ├── MIXED_AADHAR...pt    # AI Model
│   └── /uploads & /masked   # Processing Directories
│
├── /frontend                # Web Interface
│   ├── index.html           # Main UI
│   └── /assets              # CSS & JS
```

## How to Run

### 1. Start the Backend API
The backend requires Python and the necessary dependencies installed.

```bash
# Navigate to the backend folder
cd backend

# Run the server
python -m uvicorn main:app --reload
```
*Server will start at `http://127.0.0.1:8000`*

### 2. Start the Frontend
You can run the frontend using any simple HTTP server or VS Code Live Server.

```bash
# Open a new terminal
cd frontend

# Run a simple python server
python -m http.server 3000
```
*Visit `http://localhost:3000` in your browser.*

## Features
- **Backend**: Fast & Accurate YOLOv8 detection + OpenCV masking.
- **Frontend**: Modern Glassmorphism UI with Drag & Drop support.
