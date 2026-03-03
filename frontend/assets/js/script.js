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
    const extractedContainer = document.getElementById('extracted-data-container');

    // ✅ UPDATED API URL (Dynamic based on environment)
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const PROD_API_URL = 'https://aadhaar-mask-detector-fullstack.onrender.com/mask/';
    const API_URL = isLocalhost ? 'http://127.0.0.1:8000/mask/' : PROD_API_URL;


    // ===============================
    // Click to open file dialog
    // ===============================
    dropZone.addEventListener('click', () => fileInput.click());


    // ===============================
    // Drag & Drop Handling
    // ===============================
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


    // ===============================
    // File Input Handling
    // ===============================
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });


    // ===============================
    // Reset Button
    // ===============================
    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        processingSection.classList.add('hidden');
        dropZone.style.display = 'block';
        extractedContainer.classList.add('hidden');
        fileInput.value = '';
        previewImg.src = '';
    });


    // ===============================
    // Handle Selected File
    // ===============================
    function handleFile(file) {

        // Validate image
        if (!file.type.startsWith('image/')) {
            showError('Please upload a valid image file (PNG, JPG).');
            return;
        }

        const reader = new FileReader();

        reader.onload = (e) => {
            previewImg.src = e.target.result;
            dropZone.style.display = 'none';
            processingSection.classList.remove('hidden');
            loader.classList.remove('hidden');

            uploadImage(file);
        };

        reader.readAsDataURL(file);
    }


    // ===============================
    // Upload Image to Backend
    // ===============================
    async function uploadImage(file) {

        const formData = new FormData();
        formData.append('file', file);

        try {

            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Server failed to process image.');
            }

            const data = await response.json();

            if (!data.masked_image) {
                throw new Error('Invalid response from server.');
            }

            // Convert base64 to image
            const imageUrl = `data:image/png;base64,${data.masked_image}`;

            resultImg.src = imageUrl;
            downloadBtn.href = imageUrl;

            // Show extracted data
            if (data.extracted_data) {
                extractedContainer.classList.remove('hidden');

                document.getElementById('ext-name').textContent =
                    data.extracted_data.name || 'Not Found';

                document.getElementById('ext-dob').textContent =
                    data.extracted_data.dob || 'Not Found';

                document.getElementById('ext-gender').textContent =
                    data.extracted_data.gender || 'Not Found';

                document.getElementById('ext-age').textContent =
                    data.extracted_data.age || 'Not Calculated';
            } else {
                extractedContainer.classList.add('hidden');
            }

            // Hide loader and show result
            loader.classList.add('hidden');
            processingSection.classList.add('hidden');
            resultSection.classList.remove('hidden');

        } catch (error) {

            console.error(error);
            showError(error.message || 'Something went wrong.');

            loader.classList.add('hidden');
            processingSection.classList.add('hidden');
            dropZone.style.display = 'block';
        }
    }


    // ===============================
    // Show Error Toast
    // ===============================
    function showError(message) {
        errorMsg.textContent = message;
        errorToast.classList.remove('hidden');

        setTimeout(() => {
            errorToast.classList.add('hidden');
        }, 4000);
    }

});
