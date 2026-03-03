# Base Python image
FROM python:3.11-slim

# Install system dependencies, including Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port your backend uses
EXPOSE 8000

# Command to run your backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
