// import deleted

class UIController {
    constructor() {
        this.setupModal();
    }

    setupModal() {
        if (!document.getElementById('global-modal')) {
            // general alert modal (using for everything)
            const modalHTML = `
            <div id="global-modal" class="hidden fixed inset-0 bg-black bg-opacity-80 z-[60] flex items-center justify-center p-4 backdrop-blur-sm transition-all duration-300">
                <div class="bg-[#123E6B] border border-[#1E3A5F] rounded-lg max-w-sm w-full shadow-2xl transform transition-all scale-100 opacity-100 animate-[fadeIn_0.3s_ease-out]">
                    <div class="p-6 text-center">
                        <h3 id="global-modal-title" class="text-lg font-bold text-white mb-2"></h3>
                        <p id="global-modal-message" class="text-gray-300 text-sm mb-6"></p>
                        <button id="global-modal-close" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded font-bold shadow-lg transition-colors w-full">TAMAM</button>
                    </div>
                </div>
            </div>
            
            <!-- confirm modal (careful!) -->
            <div id="global-confirm-modal" class="hidden fixed inset-0 bg-black bg-opacity-80 z-[70] flex items-center justify-center p-4 backdrop-blur-sm transition-all duration-300">
                <div class="bg-[#123E6B] border border-[#1E3A5F] rounded-lg max-w-sm w-full shadow-2xl transform transition-all scale-100 opacity-100 animate-[fadeIn_0.3s_ease-out]">
                    <div class="p-6 text-center">
                        <h3 id="global-confirm-title" class="text-lg font-bold text-white mb-2"></h3>
                        <div id="global-confirm-message" class="text-gray-300 text-sm mb-6"></div>
                        <div class="flex space-x-3">
                            <button id="global-confirm-cancel" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 rounded font-bold shadow transition-colors">İPTAL</button>
                            <button id="global-confirm-ok" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded font-bold shadow transition-colors">ONAYLA</button>
                        </div>
                    </div>
                </div>
            </div>`;

            document.body.insertAdjacentHTML('beforeend', modalHTML);

            document.getElementById('global-modal-close').onclick = () => {
                document.getElementById('global-modal').classList.add('hidden');
            };

            // cancel button does nothing but hide
            document.getElementById('global-confirm-cancel').onclick = () => {
                document.getElementById('global-confirm-modal').classList.add('hidden');
            };
        }
    }

    showConfirm(title, message, onConfirm) {
        document.getElementById('global-confirm-title').textContent = title;
        document.getElementById('global-confirm-message').innerHTML = message; // Using innerHTML for formatting

        const modal = document.getElementById('global-confirm-modal');
        const okBtn = document.getElementById('global-confirm-ok');

        // clearing old listeners so button doesn't go crazy
        const newOkBtn = okBtn.cloneNode(true);
        okBtn.parentNode.replaceChild(newOkBtn, okBtn);

        newOkBtn.onclick = () => {
            modal.classList.add('hidden');
            if (onConfirm) onConfirm();
        };

        modal.classList.remove('hidden');
    }

    showModal(title, message) {
        document.getElementById('global-modal-title').textContent = title;
        document.getElementById('global-modal-message').textContent = message;
        document.getElementById('global-modal').classList.remove('hidden');
    }

    showResult(data, mode) {
        const resultsArea = document.getElementById('results-area');
        resultsArea.classList.remove('hidden');

        if (mode === 'image') {
            this.renderImageResult(data);
        } else {
            this.renderVideoResult(data);
        }
    }

    renderImageResult(data) {
        const container = document.getElementById('results-content');
        const imgDisplay = document.getElementById('result-image-display');

        imgDisplay.src = data.image; // assuming base64 or url
        imgDisplay.classList.remove('hidden');

        let html = '';
        if (data.detections && data.detections.length > 0) {
            html += `<h3 class="text-lg font-bold text-white mb-2">Tespit Edilen Plakalar</h3>`;
            html += `<div class="space-y-3">`;

            data.detections.forEach(det => {
                html += `
                <div class="bg-blue-800 p-4 rounded border border-blue-600 flex justify-between items-center">
                    <div>
                        <div class="text-2xl font-mono font-bold text-white tracking-widest">${det.text}</div>
                        <div class="text-sm text-gray-400 mt-1">${det.category} &bull; ${det.city}</div>
                    </div>
                    <button onclick="window.submitComplaint('${det.text}')" 
                        class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm font-medium transition-colors">
                        Şikayet Oluştur
                    </button>
                </div>`;
            });
            html += `</div>`;
        } else {
            html = '<div class="text-yellow-400 p-4 bg-yellow-900/20 rounded border border-yellow-800">Plaka tespit edilemedi.</div>';
        }

        container.innerHTML = html;

        // global binding (couldn't find another way)
        window.submitComplaint = (plate) => complaints.submitComplaint(plate);
    }

    renderVideoResult(data) {
        const container = document.getElementById('results-content');
        const imgDisplay = document.getElementById('result-image-display');

        imgDisplay.classList.add('hidden'); // no single image for video, hiding it

        let html = '';
        if (data.results && data.results.length > 0) {
            html += `<h3 class="text-lg font-bold text-white mb-2">Video Tespit Sonuçları (${data.results.length} Araç)</h3>`;
            html += `<div class="overflow-x-auto"><table class="w-full text-left text-sm text-gray-400">`;
            html += `<thead class="bg-blue-900 text-gray-200 uppercase"><tr><th class="p-3">Görsel</th><th class="p-3">Plaka</th><th class="p-3">Skor</th><th class="p-3">İşlem</th></tr></thead>`;
            html += `<tbody class="divide-y divide-blue-800">`;

            data.results.forEach(res => {
                html += `
                <tr class="hover:bg-blue-900/50">
                    <td class="p-3"><img src="${res.image}" class="h-8 rounded border border-gray-600"></td>
                    <td class="p-3 font-mono font-bold text-white text-base">${res.text}</td>
                    <td class="p-3">${(res.score * 100).toFixed(0)}%</td>
                    <td class="p-3">
                         <button onclick="window.submitComplaint('${res.text}')" 
                        class="text-red-400 hover:text-red-300 font-medium underline">
                        Şikayet Et
                    </button>
                    </td>
                </tr>`;
            });
            html += `</tbody></table></div>`;
        } else {
            html = '<div class="text-yellow-400 p-4 bg-yellow-900/20 rounded border border-yellow-800">Videoda araç tespit edilemedi.</div>';
        }

        container.innerHTML = html;
        window.submitComplaint = (plate) => window.complaints.submitComplaint(plate);
    }
}

window.UIController = UIController;
