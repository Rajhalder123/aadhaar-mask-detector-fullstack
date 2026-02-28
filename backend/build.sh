#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python requirements
pip install -r requirements.txt

# Download and extract tesseract-ocr binaries locally without root privileges
echo "Installing Tesseract-OCR locally..."
mkdir -p ~/bin
mkdir -p ~/tesseract
cd ~/tesseract

# Download static tesseract binaries 
wget https://github.com/DanBloomberg/leptonica/releases/download/1.83.1/leptonica-1.83.1.tar.gz
# Wait, downloading precompiled statically linked tesseract is better.
# Many projects use a simple apt-get wrapper for Render like render-apt.
# Instead, an easier trick on Render native Python is to download the ubuntu deb packages and extract them locally.

# Let's use an established strategy on Render for Python environments:
# Create a local apt directory
mkdir -p ~/.apt/usr/bin
mkdir -p ~/.apt/usr/share/tesseract-ocr/4.00/tessdata
mkdir -p ~/.apt/usr/lib

# Download and extract the debian packages for tesseract dynamically
cd /tmp
# apt-get download fetches the latest version for the current distro architecture natively without root
apt-get download tesseract-ocr libtesseract4 tesseract-ocr-eng tesseract-ocr-osd liblept5

# Extract all downloaded deb files into the local apt directory
for f in *.deb; do dpkg -x "$f" ~/.apt/; done

# Clean up
rm *.deb

echo "Tesseract installed locally."
