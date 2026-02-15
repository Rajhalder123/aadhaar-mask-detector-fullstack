# Aadhaar Masking Frontend

A modern, glassmorphism-styled frontend for the Aadhaar Masking API.

## Features
- 🎨 **Glassmorphism UI**: Premium visual aesthetics with animated backgrounds.
- 📂 **Drag & Drop**: Easy file upload interaction.
- ⚡ **Real-time Processing**: Instant feedback with loading states.
- 📱 **Responsive**: Works seamlessly on Desktop and Mobile.
- 🔒 **Secure**: Client-side processing (masked image is returned directly).

## How to Run

### Prerequisite
Ensure your backend API is running:
```bash
# In the root project directory
python -m uvicorn main:app --reload
```

### Option 1: VS Code Live Server (Recommended)
1. Open the `frontend/index.html` file in VS Code.
2. Right-click and select **"Open with Live Server"**.

### Option 2: Python HTTP Server
If you don't have Live Server, you can use Python:

1. Open a new terminal.
2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
3. Start a simple server:
   ```bash
   python -m http.server 3000
   ```
4. Open your browser and go to: `http://localhost:3000`

### Option 3: Direct File Open
You can simply double-click `index.html` to open it in your browser.
*Note: Some browsers might restrict API calls from file paths. If it fails, use Option 1 or 2.*

## Tech Stack
- **HTML5**: Semantic structure.
- **CSS3**: Variables, Flexbox/Grid, Animations.
- **JavaScript (ES6+)**: Fetch API, DOM Manipulation.
