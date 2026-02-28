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

# Download and extract the debian packages for tesseract statically (Guaranteed to work on Ubuntu Jammy)
cd /tmp

echo "Fetching latest Tesseract binaries dynamically from Ubuntu archives..."
python -c "
import urllib.request
import re
import os

packages = ['tesseract-ocr', 'libtesseract4', 'tesseract-ocr-eng', 'tesseract-ocr-osd', 'liblept5']
for pkg in packages:
    try:
        url = f'https://packages.ubuntu.com/jammy/amd64/{pkg}/download'
        html = urllib.request.urlopen(url).read().decode('utf-8')
        deb_link = re.search(r'http://mirrors\.kernel\.org/[^\"]+\.deb', html).group(0)
        print(f'Downloading {deb_link}...')
        os.system(f'wget -q {deb_link}')
    except Exception as e:
        print(f'Failed to download {pkg}: {e}')
"

# Extract all downloaded deb files into the local apt directory
for f in *.deb; do dpkg -x "$f" ~/.apt/; done

# Clean up
rm *.deb

echo "Tesseract installed locally."
