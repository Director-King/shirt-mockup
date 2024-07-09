document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const fileInput = document.getElementById('fileInput');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const originalWidthInput = document.getElementById('originalWidth');
    const originalHeightInput = document.getElementById('originalHeight');

    const PIXELS_PER_INCH = 96;
    const MAX_WIDTH = 105;
    const MAX_HEIGHT = 72;

    function inchesToPixels(inches) {
        return Math.round(inches * PIXELS_PER_INCH);
    }

    function pixelsToInches(pixels) {
        return (pixels / PIXELS_PER_INCH).toFixed(2);
    }

    function resizeImage(img, maxWidth, maxHeight) {
        let width = img.width;
        let height = img.height;
        let aspectRatio = width / height;

        if (width > maxWidth) {
            width = maxWidth;
            height = width / aspectRatio;
        }

        if (height > maxHeight) {
            height = maxHeight;
            width = height * aspectRatio;
        }

        return { width: Math.round(width), height: Math.round(height) };
    }

    form.addEventListener('submit', function (event) {
        const file = fileInput.files[0];
        const width = widthInput.value;
        const height = heightInput.value;
        const x = document.getElementById('x').value;
        const y = document.getElementById('y').value;

        if (!file) {
            alert('Please select a file.');
            event.preventDefault();
            return;
        }

        if (file.type !== 'image/png') {
            alert('Only PNG files are allowed!');
            event.preventDefault();
            return;
        }

        if (!width || !height || !x || !y) {
            alert('Please fill in all dimensions and position fields.');
            event.preventDefault();
            return;
        }

        // Convert inches to pixels before submitting
        widthInput.value = inchesToPixels(width);
        heightInput.value = inchesToPixels(height);
        document.getElementById('x').value = inchesToPixels(x);
        document.getElementById('y').value = inchesToPixels(y);
    });

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file && file.type === 'image/png') {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = new Image();
                img.onload = function() {
                    const resizedDimensions = resizeImage(img, MAX_WIDTH, MAX_HEIGHT);
                    
                    const canvas = document.createElement('canvas');
                    canvas.width = resizedDimensions.width;
                    canvas.height = resizedDimensions.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, resizedDimensions.width, resizedDimensions.height);
                    
                    const previewContainer = document.querySelector('.preview-container');
                    if (previewContainer) {
                        previewContainer.innerHTML = '';
                        const previewImg = new Image();
                        previewImg.src = canvas.toDataURL('image/png');
                        previewImg.style.maxWidth = '300px';
                        previewImg.style.maxHeight = '300px';
                        previewContainer.appendChild(previewImg);
                    }
                    
                    // Set default size to resized image dimensions
                    widthInput.value = pixelsToInches(resizedDimensions.width);
                    heightInput.value = pixelsToInches(resizedDimensions.height);
                    
                    // Store original dimensions
                    originalWidthInput.value = img.width;
                    originalHeightInput.value = img.height;
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            alert('Only PNG files are allowed!');
            fileInput.value = '';
        }
    });
});