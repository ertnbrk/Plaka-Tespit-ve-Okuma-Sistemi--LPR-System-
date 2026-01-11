import Swal from 'sweetalert2'
import './style.css'
import { uploadImage, uploadVideo, queryVehicleData } from './api.js'

// --- State ---
const state = {
  mode: 'image', // 'image' or 'video'
  selectedFile: null,
  loading: false,
  error: null,
  resultImage: null,
  imageDetections: [],
  videoResults: [],
  modal: {
    visible: false,
    loading: false,
    data: null
  }
};

// --- DOM Elements ---
const dom = {
  tabImage: document.getElementById('tab-image'),
  tabVideo: document.getElementById('tab-video'),
  warningVideo: document.getElementById('section-warning-video'),
  dropZone: document.getElementById('drop-zone'),
  inputFile: document.getElementById('input-file'),
  iconMode: document.getElementById('icon-mode'),
  labelMode: document.getElementById('label-mode'),
  dropZoneTextDefault: document.getElementById('drop-zone-text-default'),
  dropZoneTextFile: document.getElementById('drop-zone-text-file'),
  fileName: document.getElementById('file-name'),
  btnProcess: document.getElementById('btn-process'),
  btnProcessText: document.getElementById('btn-process-text'),
  btnProcessSpinner: document.getElementById('btn-process-spinner'),
  btnProcessLoadingText: document.getElementById('btn-process-loading-text'),
  errorMessage: document.getElementById('error-message'),
  resultsImageSection: document.getElementById('results-image-section'),
  resultImage: document.getElementById('result-image'),
  resultDetectionsList: document.getElementById('result-detections-list'),
  resultsVideoSection: document.getElementById('results-video-section'),
  videoResultsCount: document.getElementById('video-results-count'),
  resultsVideoTableBody: document.getElementById('results-video-table-body'),
  modal: document.getElementById('modal'),
  btnModalClose: document.getElementById('btn-modal-close'),
  modalContentLoading: document.getElementById('modal-content-loading'),
  modalContentData: document.getElementById('modal-content-data'),
  modalPlate: document.getElementById('modal-plate'),
  modalVehicleTitle: document.getElementById('modal-vehicle-title'),
  modalVehicleInfo: document.getElementById('modal-vehicle-info'),
  modalMileage: document.getElementById('modal-mileage'),
  modalMileageDate: document.getElementById('modal-mileage-date'),
  modalDamageContainer: document.getElementById('modal-damage-container'),
  modalDamageTitle: document.getElementById('modal-damage-title'),
  modalDamageCount: document.getElementById('modal-damage-count'),
  modalTimelineSection: document.getElementById('modal-timeline-section'),
  modalNoDamage: document.getElementById('modal-no-damage')
};

// --- Logic ---

function updateUI() {
  // Tabs
  if (state.mode === 'image') {
    dom.tabImage.className = 'flex-1 py-4 px-6 text-center font-medium transition-colors text-blue-600 border-b-2 border-blue-600';
    dom.tabVideo.className = 'flex-1 py-4 px-6 text-center font-medium transition-colors text-gray-500 hover:text-gray-700';
    dom.warningVideo.classList.add('hidden');
    dom.iconMode.textContent = '🖼️';
    dom.labelMode.textContent = 'Resim yüklemek için tıklayın veya sürükleyin';
    dom.btnProcessText.textContent = 'Resmi Analiz Et';
    dom.btnProcessLoadingText.textContent = 'İşleniyor...';
    dom.inputFile.accept = 'image/*';
  } else {
    dom.tabImage.className = 'flex-1 py-4 px-6 text-center font-medium transition-colors text-gray-500 hover:text-gray-700';
    dom.tabVideo.className = 'flex-1 py-4 px-6 text-center font-medium transition-colors text-blue-600 border-b-2 border-blue-600';
    dom.warningVideo.classList.remove('hidden');
    dom.iconMode.textContent = '🎬';
    dom.labelMode.textContent = 'Video yüklemek için tıklayın veya sürükleyin';
    dom.btnProcessText.textContent = 'Videoyu Analiz Et';
    dom.btnProcessLoadingText.textContent = 'Video İşleniyor...';
    dom.inputFile.accept = 'video/*';
  }

  // File Input Visuals
  if (state.selectedFile) {
    dom.dropZoneTextDefault.classList.add('hidden');
    dom.dropZoneTextFile.classList.remove('hidden');
    dom.fileName.textContent = state.selectedFile.name;
    dom.btnProcess.disabled = state.loading;
  } else {
    dom.dropZoneTextDefault.classList.remove('hidden');
    dom.dropZoneTextFile.classList.add('hidden');
    dom.fileName.textContent = '';
    dom.btnProcess.disabled = true;
  }

  // Loading State
  if (state.loading) {
    dom.btnProcessSpinner.classList.remove('hidden');
    dom.btnProcessText.classList.add('hidden');
    dom.btnProcess.disabled = true;
  } else {
    dom.btnProcessSpinner.classList.add('hidden');
    dom.btnProcessText.classList.remove('hidden');
  }

  // Error Message
  if (state.error) {
    dom.errorMessage.textContent = state.error;
    dom.errorMessage.classList.remove('hidden');
  } else {
    dom.errorMessage.classList.add('hidden');
  }

  // Results: Image
  if (state.mode === 'image' && state.resultImage) {
    dom.resultsImageSection.classList.remove('hidden');
    dom.resultImage.src = state.resultImage;
    renderImageDetections();
  } else {
    dom.resultsImageSection.classList.add('hidden');
  }

  // Results: Video
  if (state.mode === 'video' && state.videoResults.length > 0) {
    dom.resultsVideoSection.classList.remove('hidden');
    dom.videoResultsCount.textContent = state.videoResults.length;
    renderVideoDetections();
  } else {
    dom.resultsVideoSection.classList.add('hidden');
  }

  // Modal
  if (state.modal.visible) {
    dom.modal.classList.remove('hidden');
    if (state.modal.loading) {
      dom.modalContentLoading.classList.remove('hidden');
      dom.modalContentData.classList.add('hidden');
    } else {
      dom.modalContentLoading.classList.add('hidden');
      if (state.modal.data) {
        dom.modalContentData.classList.remove('hidden');
        renderModalData();
      }
    }
  } else {
    dom.modal.classList.add('hidden');
  }
}

function renderImageDetections() {
  dom.resultDetectionsList.innerHTML = '';
  
  if (state.imageDetections.length === 0) {
    dom.resultDetectionsList.innerHTML = '<div class="text-gray-500 italic">Plaka bulunamadı.</div>';
    return;
  }

  state.imageDetections.forEach(det => {
    const card = document.createElement('div');
    card.className = 'mb-6 last:mb-0 bg-white p-4 rounded shadow-sm border border-gray-100';
    
    // Category Badge
    const isStandard = det.category.includes('Standard');
    const badgeClass = isStandard ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800';

    card.innerHTML = `
      <div class="mb-1">
        <span class="text-sm text-gray-500 uppercase font-bold tracking-wider">Metin</span>
        <div class="text-3xl font-mono font-bold text-gray-900 break-all">${det.text}</div>
      </div>
      
      <div class="mb-3">
        <span class="text-xs text-gray-500 uppercase">Şehir / Bölge</span>
        ${det.city !== 'Unknown' 
          ? `<div class="text-lg font-semibold text-blue-700 flex items-center"><span class="text-xl mr-2">📍</span> ${det.city}</div>`
          : '<div class="text-gray-400">Bilinmiyor</div>'
        }
      </div>
      
      <div class="mb-4">
        <span class="text-xs text-gray-500 uppercase">Kategori</span>
        <div class="mt-1">
          <span class="px-2 py-1 text-sm font-semibold rounded ${badgeClass}">
            ${det.category}
          </span>
        </div>
      </div>

      <button class="btn-query w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition flex justify-center items-center" data-plate="${det.text}">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        Hasar & Araç Sorgula
      </button>
    `;
    dom.resultDetectionsList.appendChild(card);
  });
}

function renderVideoDetections() {
  dom.resultsVideoTableBody.innerHTML = '';
  state.videoResults.forEach(item => {
    const tr = document.createElement('tr');
    tr.className = 'hover:bg-gray-50';
    
    const isStandard = item.category.includes('Standard');
    const badgeClass = isStandard ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800';

    tr.innerHTML = `
      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#${item.track_id}</td>
      <td class="px-6 py-4 whitespace-nowrap"><img src="${item.image}" class="h-10 rounded border border-gray-300"></td>
      <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 font-mono text-lg">${item.text}</td>
      <td class="px-6 py-4 whitespace-nowrap">
        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${badgeClass}">
          ${item.category}
        </span>
      </td>
      <td class="px-6 py-4 whitespace-nowrap">
        <button class="btn-query text-indigo-600 hover:text-indigo-900 font-medium text-sm" data-plate="${item.text}">Sorgula ➜</button>
      </td>
    `;
    dom.resultsVideoTableBody.appendChild(tr);
  });
}

function renderModalData() {
  const data = state.modal.data;
  if (!data) return;

  dom.modalPlate.textContent = data.plate;
  dom.modalVehicleTitle.textContent = `${data.vehicle.brand} ${data.vehicle.model}`;
  dom.modalVehicleInfo.textContent = `${data.vehicle.year} • ${data.vehicle.fuelType} • ${data.vehicle.color}`;
  
  dom.modalMileage.textContent = `${data.mileage.value.toLocaleString()} KM`;
  dom.modalMileageDate.textContent = `Son Kontrol: ${data.mileage.lastUpdated}`;

  const hasDamage = data.damageStatus.hasDamage;
  
  if (hasDamage) {
    dom.modalDamageContainer.className = 'p-4 rounded-lg bg-red-50';
    dom.modalDamageTitle.className = 'text-xs uppercase font-bold text-red-500';
    dom.modalDamageCount.className = 'text-2xl font-bold text-red-900';
    dom.modalDamageCount.textContent = `${data.damageStatus.damageCount} ADET KAYIT`;
    
    dom.modalTimelineSection.innerHTML = '';
    const h4 = document.createElement('h4');
    h4.className = 'text-sm font-bold text-gray-500 uppercase mb-3';
    h4.textContent = 'Hasar Geçmişi Timeline';
    dom.modalTimelineSection.appendChild(h4);

    const divSpace = document.createElement('div');
    divSpace.className = 'space-y-3';
    
    data.damageStatus.records.forEach(rec => {
      divSpace.innerHTML += `
        <div class="flex items-start">
          <div class="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-red-400 mr-3"></div>
          <div class="flex-1 bg-gray-50 p-3 rounded text-sm">
            <div class="flex justify-between">
              <span class="font-bold text-gray-800">${rec.date}</span>
              <span class="font-bold text-red-600">${rec.cost}</span>
            </div>
            <div class="text-gray-600 mt-1">
              ${rec.type} - <span class="text-gray-800">${rec.location}</span> (${rec.severity})
            </div>
          </div>
        </div>
      `;
    });
    dom.modalTimelineSection.appendChild(divSpace);
    dom.modalNoDamage.classList.add('hidden');
  } else {
    dom.modalDamageContainer.className = 'p-4 rounded-lg bg-green-50';
    dom.modalDamageTitle.className = 'text-xs uppercase font-bold text-green-500';
    dom.modalDamageCount.className = 'text-2xl font-bold text-green-900';
    dom.modalDamageCount.textContent = 'TEMİZ';

    dom.modalTimelineSection.innerHTML = '';
    dom.modalNoDamage.classList.remove('hidden');
  }
}

// --- Event Handlers ---

dom.tabImage.addEventListener('click', () => {
  state.mode = 'image';
  resetResults();
  updateUI();
});

dom.tabVideo.addEventListener('click', () => {
  state.mode = 'video';
  resetResults();
  updateUI();
});

function resetResults() {
  state.selectedFile = null;
  state.resultImage = null;
  state.imageDetections = [];
  state.videoResults = [];
  state.error = null;
  // Reset input
  dom.inputFile.value = '';
}

dom.inputFile.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    state.selectedFile = file;
    state.error = null;
    updateUI();
  }
});

// Process Button
dom.btnProcess.addEventListener('click', async () => {
  if (!state.selectedFile) return;

  state.loading = true;
  state.error = null;
  state.resultImage = null;
  state.imageDetections = [];
  state.videoResults = [];
  updateUI();

  try {
    let data;
    if (state.mode === 'image') {
      data = await uploadImage(state.selectedFile);
    } else {
      data = await uploadVideo(state.selectedFile);
    }

    if (data.error) throw new Error(data.error);

    if (state.mode === 'image') {
      state.resultImage = data.image;
      state.imageDetections = data.detections || [];
    } else {
      state.videoResults = data.results;
    }

  } catch (err) {
    console.error(err);
    state.error = 'Hata: ' + err.message;
  } finally {
    state.loading = false;
    updateUI();
  }
});

// Event Delegation for "Query" buttons in results lists
document.addEventListener('click', async (e) => {
  if (e.target.matches('.btn-query') || e.target.closest('.btn-query')) {
    const btn = e.target.matches('.btn-query') ? e.target : e.target.closest('.btn-query');
    const plate = btn.dataset.plate;
    if (plate) {
      await queryVehicle(plate);
    }
  }
});

// Modal Close
dom.btnModalClose.addEventListener('click', () => {
  state.modal.visible = false;
  updateUI();
});

async function queryVehicle(plateText) {
  state.modal.visible = true;
  state.modal.loading = true;
  state.modal.data = null;
  updateUI();

  try {
    const data = await queryVehicleData(plateText);

    if (data.status === 'NOT_FOUND' || data.error) {
      Swal.fire({
        icon: 'warning',
        title: 'Kayıt Bulunamadı',
        text: 'Bu plakaya ait kayıt bulunamadı (Demo veritabanı).',
        confirmButtonText: 'Tamam',
        confirmButtonColor: '#3085d6'
      });
      state.modal.visible = false;
    } else {
      state.modal.data = data;
    }
  } catch (err) {
    Swal.fire({
      icon: 'error',
      title: 'Hata',
      text: 'Sorgu hatası: ' + err.message,
      confirmButtonText: 'Tamam'
    });
    state.modal.visible = false;
  } finally {
    state.modal.loading = false;
    updateUI();
  }
}