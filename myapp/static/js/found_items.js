document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('dropzone-file');
    const dropzonePrompt = document.getElementById('dropzone-prompt');
    const filePreview = document.getElementById('file-preview');
    const previewImg = document.getElementById('preview-img');
    const fileName = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const aiScanner = document.getElementById('ai-scanner');

    const titleInput = document.getElementById('title');
    const categoryInput = document.getElementById('category');
    const badgeTitle = document.getElementById('ai-badge-title');
    const badgeCategory = document.getElementById('ai-badge-category');

    let dragCounter = 0; 

    // 1. Block default browser open-file behavior on entire window
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        window.addEventListener(eventName, (e) => e.preventDefault(), false);
        dropzone.addEventListener(eventName, (e) => e.preventDefault(), false);
    });

    // 2. Drag Enter
    dropzone.addEventListener('dragenter', (e) => {
        e.preventDefault();
        dragCounter++;
        dropzone.classList.add('border-indigo-500', 'bg-indigo-50/80');
    });

    // 3. Drag Over
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    // 4. Drag Leave
    dropzone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dragCounter--;
        if (dragCounter === 0) {
            dropzone.classList.remove('border-indigo-500', 'bg-indigo-50/80');
        }
    });

    // 5. Drop Event (Fixes file assignment bug)
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dragCounter = 0;
        dropzone.classList.remove('border-indigo-500', 'bg-indigo-50/80');

        const droppedFiles = e.dataTransfer.files;
        if (droppedFiles && droppedFiles.length > 0) {
            // Re-assign file using DataTransfer object
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(droppedFiles[0]);
            fileInput.files = dataTransfer.files;

            processFile(droppedFiles[0]);
        }
    });

    // 6. Manual File Picker Click
    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            processFile(e.target.files[0]);
        }
    });

    // 7. Preview & Trigger AI
    function processFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (PNG, JPG, WEBP).');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            fileName.textContent = file.name;

            dropzonePrompt.classList.add('hidden');
            filePreview.classList.remove('hidden');
            filePreview.classList.add('flex');

            // Trigger AI analysis function
            runAiDetection(file);
        };
        reader.readAsDataURL(file);
    }

    // 8. Reset File Selection
    removeFileBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        fileInput.value = '';
        previewImg.src = '#';
        fileName.textContent = '';

        filePreview.classList.add('hidden');
        filePreview.classList.remove('flex');
        dropzonePrompt.classList.remove('hidden');

        // Clear values and badges
        titleInput.value = '';
        categoryInput.value = '';
        badgeTitle.classList.add('hidden');
        badgeCategory.classList.add('hidden');
    });

    // 9. AI API Request Handler
    async function runAiDetection(file) {
        aiScanner.classList.remove('hidden');

        
        // ===================================================================
        // Django API Integration Code:
        // ===================================================================
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/detect-item/', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                titleInput.value = data.title;
                categoryInput.value = data.category;

                badgeTitle.classList.remove('hidden');
                badgeCategory.classList.remove('hidden');
                // testing code
            }
        } catch (error) {
            console.error('Error contacting AI service:', error);
        } finally {
            aiScanner.classList.add('hidden');
        }
    

        // Local testing simulation delay
        // setTimeout(() => {
        //     titleInput.value = "Black Leather School Bag";
        //     categoryInput.value = "Bags & Backpacks";

        //     badgeTitle.classList.remove('hidden');
        //     badgeCategory.classList.remove('hidden');
        //     aiScanner.classList.add('hidden');

        // }, 1200);
    }
});