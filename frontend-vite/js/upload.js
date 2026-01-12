// import gone

class UploadController {
    constructor(successCallback) {
        this.successCallback = successCallback;
        this.bindEvents();
    }

    bindEvents() {
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file-input');
        const analyzeBtn = document.getElementById('analyze-btn');
        const tabImage = document.getElementById('tab-image');
        const tabVideo = document.getElementById('tab-video');

        if (!dropZone || !fileInput) return;

        this.currentMode = 'image'; // image or video

        // Tabs for switching between image/video
        tabImage?.addEventListener('click', () => {
            this.setMode('image');
            tabImage.classList.add('bg-blue-900', 'text-white');
            tabImage.classList.remove('bg-gray-800', 'text-gray-400');
            tabVideo.classList.remove('bg-blue-900', 'text-white');
            tabVideo.classList.add('bg-gray-800', 'text-gray-400');
        });

        tabVideo?.addEventListener('click', () => {
            this.setMode('video');
            tabVideo.classList.add('bg-blue-900', 'text-white');
            tabVideo.classList.remove('bg-gray-800', 'text-gray-400');
            tabImage.classList.remove('bg-blue-900', 'text-white');
            tabImage.classList.add('bg-gray-800', 'text-gray-400');
        });

        // drag & drop stuff
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-red-500');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-red-500');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-red-500');
            if (e.dataTransfer.files.length) {
                this.handleFileSelect(e.dataTransfer.files[0]);
            }
        });

        dropZone.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                this.handleFileSelect(e.target.files[0]);
            }
        });

        analyzeBtn?.addEventListener('click', () => this.analyze());
    }

    setMode(mode) {
        this.currentMode = mode;
        const fileInput = document.getElementById('file-input');
        const warning = document.getElementById('video-warning');

        fileInput.value = '';
        this.selectedFile = null;
        this.updateFileDisplay();

        if (mode === 'image') {
            fileInput.accept = 'image/*';
            warning.classList.add('hidden');
        } else {
            fileInput.accept = 'video/*';
            warning.classList.remove('hidden');
        }
    }

    handleFileSelect(file) {
        // checking file type (no weird files)
        if (this.currentMode === 'image' && !file.type.startsWith('image/')) {
            if (window.ui) window.ui.showModal('Hata', 'Lütfen resim dosyası seçiniz.');
            else alert('Lütfen resim dosyası seçiniz.');
            return;
        }
        if (this.currentMode === 'video' && !file.type.startsWith('video/')) {
            if (window.ui) window.ui.showModal('Hata', 'Lütfen video dosyası seçiniz.');
            else alert('Lütfen video dosyası seçiniz.');
            return;
        }

        this.selectedFile = file;
        this.updateFileDisplay();
    }

    updateFileDisplay() {
        const display = document.getElementById('file-name-display');
        const analyzeBtn = document.getElementById('analyze-btn');

        if (this.selectedFile) {
            display.textContent = `Seçilen Dosya: ${this.selectedFile.name}`;
            display.classList.remove('hidden');
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            analyzeBtn.classList.add('hover:bg-red-700');
        } else {
            display.classList.add('hidden');
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('opacity-50', 'cursor-not-allowed');
            analyzeBtn.classList.remove('hover:bg-red-700');
        }
    }

    async analyze() {
        if (!this.selectedFile) return;

        const spinner = document.getElementById('loading-spinner');
        const resultsArea = document.getElementById('results-area');

        spinner.classList.remove('hidden');
        resultsArea.classList.add('hidden');

        try {
            let result;
            if (this.currentMode === 'image') {
                result = await window.api.detectImage(this.selectedFile);
            } else {
                result = await window.api.detectVideo(this.selectedFile);
            }

            this.successCallback(result, this.currentMode);
        } catch (error) {
            if (window.ui) window.ui.showModal('Analiz Hatası', error.message);
            else alert('Analiz hatası: ' + error.message);
        } finally {
            spinner.classList.add('hidden');
        }
    }
}

// Global scope
window.UploadController = UploadController;
