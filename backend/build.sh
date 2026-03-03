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
# Create a local apt directory inside the current folder
export APT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.apt"
mkdir -p "$APT_DIR/usr/bin"
mkdir -p "$APT_DIR/usr/share/tesseract-ocr/4.00/tessdata"
mkdir -p "$APT_DIR/usr/lib"

# Download and extract the debian packages for tesseract statically (Guaranteed to work on Ubuntu Jammy)
cd /tmp

echo "Fetching Tesseract binaries directly from Ubuntu mirrors..."

# We bypass packages.ubuntu.com because Render often gets hit with HTTP 500/rate limits
wget -q http://mirrors.kernel.org/ubuntu/pool/universe/t/tesseract/tesseract-ocr_4.1.1-2.1build1_amd64.deb
wget -q http://mirrors.kernel.org/ubuntu/pool/universe/t/tesseract/libtesseract4_4.1.1-2.1build1_amd64.deb
wget -q http://mirrors.kernel.org/ubuntu/pool/main/t/tesseract-lang/tesseract-ocr-eng_4.00~git30-7274cfa-1.1_all.deb
wget -q http://mirrors.kernel.org/ubuntu/pool/main/t/tesseract-lang/tesseract-ocr-osd_4.00~git30-7274cfa-1.1_all.deb
wget -q http://mirrors.kernel.org/ubuntu/pool/universe/l/leptonica/liblept5_1.82.0-3build1_amd64.deb

# Extract all downloaded deb files into the local apt directory
for f in *.deb; do dpkg -x "$f" "$APT_DIR/"; done

# Clean up
rm *.deb

echo "Tesseract installed locally."
