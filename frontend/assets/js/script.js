document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const processingSection = document.getElementById('processing-section');
    const loader = document.getElementById('loader');
    const previewImg = document.getElementById('preview-img');
    const resultSection = document.getElementById('result-section');
    const resultImg = document.getElementById('result-img');
    const downloadBtn = document.getElementById('download-btn');
    const resetBtn = document.getElementById('reset-btn');
    const errorToast = document.getElementById('error-toast');
    const errorMsg = document.getElementById('error-msg');

    const API_URL = 'http://127.0.0.1:8000/mask/';

    // Trigger file input on click
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag & Drop Handling
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File Input Handling
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Reset Button
    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        dropZone.style.display = 'block';
        processingSection.classList.add('hidden');
        fileInput.value = ''; // Reset input
    });

    function handleFile(file) {
        // Validate file type
        if (!file.type.match('image.*')) {
            showError('Please upload a valid image file (PNG, JPG).');
            return;
        }

        // Show Preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            dropZone.style.display = 'none';
            processingSection.classList.remove('hidden');
            loader.classList.remove('hidden'); // Show loader

            // Upload to API
            uploadImage(file);
        };
        reader.readAsDataURL(file);
    }

    async function uploadImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Server Failed to Process Image');
            }

            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);

            // Update Result
            resultImg.src = imageUrl;
            downloadBtn.href = imageUrl;

            // Show Result Section
            loader.classList.add('hidden');
            previewImg.src = ''; // Clear preview memory
            processingSection.classList.add('hidden');
            resultSection.classList.remove('hidden');

        } catch (error) {
            console.error(error);
            showError('Error: ' + error.message);

            // Reset UI on error
            loader.classList.add('hidden');
            processingSection.classList.add('hidden');
            dropZone.style.display = 'block';
        }
    }

    function showError(message) {
        errorMsg.textContent = message;
        errorToast.classList.remove('hidden');
        setTimeout(() => {
            errorToast.classList.add('hidden');
        }, 4000);
    }
});
