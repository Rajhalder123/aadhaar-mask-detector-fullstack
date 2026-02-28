# Use an official lightweight Python image
FROM python:3.10-slim

# Install system dependencies including Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (Render sets the PORT environment variable dynamically)
EXPOSE 8000

# Command to run the application using Uvicorn
CMD if [ -z "$PORT" ]; then uvicorn main:app --host 0.0.0.0 --port 8000; else uvicorn main:app --host 0.0.0.0 --port $PORT; fi
