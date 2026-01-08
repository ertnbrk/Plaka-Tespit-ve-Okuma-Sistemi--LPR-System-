<script setup>
import { ref, computed, watch } from 'vue'
import Swal from 'sweetalert2'

// State
const mode = ref('image') 
const selectedFile = ref(null)

// Processing Data
const resultImage = ref(null)
const imageDetections = ref([])
const videoResults = ref([])

// UI State
const loading = ref(false)
const error = ref(null)

// Modal State
const showModal = ref(false)
const queryLoading = ref(false)
const vehicleData = ref(null)

// Computed Properties for logic
const isImageMode = computed(() => mode.value === 'image')
const isVideoMode = computed(() => mode.value === 'video')

// Watchers
watch(mode, () => {
    selectedFile.value = null
    resultImage.value = null
    imageDetections.value = []
    videoResults.value = []
    error.value = null
})

// Handlers
const onFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
        selectedFile.value = file
        error.value = null
    }
}

const processUpload = async () => {
    if (!selectedFile.value) return

    loading.value = true
    error.value = null
    resultImage.value = null
    imageDetections.value = []
    videoResults.value = []
    
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const endpoint = isImageMode.value 
        ? 'http://localhost:8000/predict' 
        : 'http://localhost:8000/predict_video'

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        })

        if (!response.ok) throw new Error('Sunucu hatası: ' + response.statusText)

        const data = await response.json()
        if (data.error) throw new Error(data.error)

        if (isImageMode.value) {
            resultImage.value = data.image
            imageDetections.value = data.detections || []
        } else {
            videoResults.value = data.results
        }

    } catch (err) {
        console.error(err)
        error.value = 'Hata: ' + err.message
    } finally {
        loading.value = false
    }
}

const queryVehicle = async (plateText) => {
    showModal.value = true
    queryLoading.value = true
    vehicleData.value = null
    
    try {
        const response = await fetch('http://localhost:8000/api/vehicle/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plate: plateText })
        })
        
        const data = await response.json()
        
        if (data.status === 'NOT_FOUND' || data.error) {
            Swal.fire({
                icon: 'warning',
                title: 'Kayıt Bulunamadı',
                text: 'Bu plakaya ait kayıt bulunamadı (Demo veritabanı).',
                confirmButtonText: 'Tamam',
                confirmButtonColor: '#3085d6'
            })
            showModal.value = false
        } else {
            vehicleData.value = data
        }
    } catch (err) {
        Swal.fire({
            icon: 'error',
            title: 'Hata',
            text: 'Sorgu hatası: ' + err.message,
            confirmButtonText: 'Tamam'
        })
        showModal.value = false
    } finally {
        queryLoading.value = false
    }
}

const closeModal = () => {
    showModal.value = false
}

// Helper Computed for Modal Logic
const damageLabel = computed(() => {
    if (!vehicleData.value) return ''
    return vehicleData.value.damageStatus.hasDamage 
        ? `${vehicleData.value.damageStatus.damageCount} ADET KAYIT` 
        : 'TEMİZ'
})

const damageClass = computed(() => {
    if (!vehicleData.value) return ''
    return vehicleData.value.damageStatus.hasDamage 
        ? 'text-red-900' 
        : 'text-green-900'
})

const damageBgClass = computed(() => {
    if (!vehicleData.value) return ''
    return vehicleData.value.damageStatus.hasDamage 
        ? 'bg-red-50' 
        : 'bg-green-50'
})

const damageTitleClass = computed(() => {
    if (!vehicleData.value) return ''
    return vehicleData.value.damageStatus.hasDamage 
        ? 'text-red-500' 
        : 'text-green-500'
})

</script>

<template>
    <div class="relative w-full max-w-6xl mx-auto p-4">
        
        <!-- Main Card -->
        <div class="bg-white p-8 rounded-lg shadow-xl w-full">
            <h1 class="text-3xl font-bold mb-6 text-center text-gray-800">Plaka Tespit Sistemi</h1>
            
            <!-- Tabs -->
            <div class="flex border-b border-gray-200 mb-6">
                <button @click="mode = 'image'" 
                    class="flex-1 py-4 px-6 text-center font-medium transition-colors"
                    :class="isImageMode ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'">
                    📷 Resim Analizi
                </button>
                <button @click="mode = 'video'" 
                    class="flex-1 py-4 px-6 text-center font-medium transition-colors"
                    :class="isVideoMode ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'">
                    🎥 Video Analizi <span class="ml-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">Test Aşamasında</span>
                </button>
            </div>

            <!-- Warning for Video Mode -->
            <div v-if="isVideoMode" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
                <div class="flex">
                    <div class="flex-shrink-0">⚠️</div>
                    <div class="ml-3">
                        <p class="text-sm text-yellow-700">
                            <strong>Dikkat:</strong> Video analizi şu an test (beta) aşamasındadır. İşlem süresi videonun uzunluğuna göre artabilir.
                        </p>
                    </div>
                </div>
            </div>

            <div class="space-y-6">
                <!-- Upload Area -->
                <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer relative">
                    <input type="file" @change="onFileChange" :accept="isImageMode ? 'image/*' : 'video/*'"
                        class="opacity-0 absolute inset-0 w-full h-full cursor-pointer">
                    
                    <div v-if="!selectedFile" class="text-gray-500">
                        <div class="mb-2">
                             <span class="text-4xl" v-if="isImageMode">🖼️</span>
                             <span class="text-4xl" v-else>🎬</span>
                        </div>
                        <p>{{ isImageMode ? 'Resim' : 'Video' }} yüklemek için tıklayın veya sürükleyin</p>
                    </div>
                    
                    <div v-else class="text-green-600 font-semibold flex items-center justify-center gap-2">
                        <span class="text-xl">✅</span>
                        {{ selectedFile.name }}
                    </div>
                </div>

                <!-- Action Button -->
                <button @click="processUpload" :disabled="!selectedFile || loading"
                    class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center">
                    <span v-if="loading" class="flex items-center">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        {{ isVideoMode ? 'Video İşleniyor...' : 'İşleniyor...' }}
                    </span>
                    <span v-else>{{ isImageMode ? 'Resmi Analiz Et' : 'Videoyu Analiz Et' }}</span>
                </button>

                <!-- Error Message -->
                <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                    {{ error }}
                </div>

                <!-- IMAGE Results (Split Layout) -->
                <div v-if="isImageMode && resultImage" class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- Left: Image -->
                    <div class="md:col-span-2">
                        <h2 class="text-xl font-semibold text-gray-700 mb-4">Görsel:</h2>
                        <div class="rounded-lg overflow-hidden border border-gray-200 shadow-sm">
                            <img :src="resultImage" alt="Processed Image" class="w-full h-auto">
                        </div>
                    </div>
                    
                    <!-- Right: Details -->
                    <div class="md:col-span-1 bg-gray-50 p-6 rounded-lg border border-gray-200">
                        <h2 class="text-xl font-semibold text-gray-700 mb-4 border-b pb-2">Plaka Bilgileri</h2>
                        
                        <div v-if="imageDetections.length === 0" class="text-gray-500 italic">
                            Plaka bulunamadı.
                        </div>

                        <div v-for="(det, index) in imageDetections" :key="index" class="mb-6 last:mb-0 bg-white p-4 rounded shadow-sm border border-gray-100">
                             <div class="mb-1">
                                <span class="text-sm text-gray-500 uppercase font-bold tracking-wider">Metin</span>
                                <div class="text-3xl font-mono font-bold text-gray-900 break-all">{{ det.text }}</div>
                            </div>
                            
                            <div class="mb-3">
                                <span class="text-xs text-gray-500 uppercase">Şehir / Bölge</span>
                                <div v-if="det.city !== 'Unknown'" class="text-lg font-semibold text-blue-700 flex items-center">
                                    <span class="text-xl mr-2">📍</span> {{ det.city }}
                                </div>
                                <div v-else class="text-gray-400">Bilinmiyor</div>
                            </div>
                            
                            <div class="mb-4">
                                <span class="text-xs text-gray-500 uppercase">Kategori</span>
                                <div class="mt-1">
                                    <span :class="['px-2 py-1 text-sm font-semibold rounded', det.category.includes('Standard') ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
                                        {{ det.category }}
                                    </span>
                                </div>
                            </div>

                            <!-- Query Button -->
                            <button @click="queryVehicle(det.text)" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition flex justify-center items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                Hasar & Araç Sorgula
                            </button>
                        </div>
                    </div>
                </div>

                <!-- VIDEO Results -->
                <div v-if="isVideoMode && videoResults.length > 0" class="mt-8 space-y-4">
                    <h2 class="text-xl font-semibold text-gray-700">Taranan Araçlar ({{ videoResults.length }} adet)</h2>
                    <div class="overflow-x-auto">
                        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Görüntü</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Plaka</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kategori</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">İşlem</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr v-for="item in videoResults" :key="item.track_id" class="hover:bg-gray-50">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{{ item.track_id }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap"><img :src="item.image" class="h-10 rounded border border-gray-300"></td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 font-mono text-lg">{{ item.text }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span :class="['px-2 inline-flex text-xs leading-5 font-semibold rounded-full', item.category.includes('Standard') ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
                                            {{ item.category }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <button @click="queryVehicle(item.text)" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">Sorgula ➜</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Vehicle Info Modal -->
        <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div class="bg-white rounded-lg shadow-2xl w-full max-w-2xl overflow-hidden transform transition-all">
                <!-- Header -->
                <div class="bg-gray-800 text-white px-6 py-4 flex justify-between items-center">
                    <h3 class="text-lg font-bold flex items-center">
                         <span class="mr-2">🚓</span> Araç & Hasar Bilgisi
                    </h3>
                    <button @click="closeModal" class="text-gray-400 hover:text-white text-2xl">&times;</button>
                </div>

                <!-- Body -->
                <div class="p-6">
                    <div v-if="queryLoading" class="flex flex-col items-center justify-center py-12">
                         <svg class="animate-spin h-10 w-10 text-indigo-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <p class="text-gray-600 animate-pulse">Emniyet Veritabanı Sorgulanıyor...</p>
                    </div>

                    <div v-else-if="vehicleData">
                        <!-- Vehicle ID -->
                        <div class="flex items-center justify-between mb-6 pb-6 border-b border-gray-100">
                             <div>
                                 <div class="text-sm text-gray-500">Plaka</div>
                                 <div class="text-3xl font-black text-gray-900 font-mono">{{ vehicleData.plate }}</div>
                             </div>
                             <div class="text-right">
                                 <div class="text-2xl font-bold text-gray-800">{{ vehicleData.vehicle.brand }} {{ vehicleData.vehicle.model }}</div>
                                 <div class="text-sm text-gray-500">{{ vehicleData.vehicle.year }} • {{ vehicleData.vehicle.fuelType }} • {{ vehicleData.vehicle.color }}</div>
                             </div>
                        </div>

                        <!-- Stats Grid -->
                        <div class="grid grid-cols-2 gap-4 mb-6">
                            <div class="bg-blue-50 p-4 rounded-lg">
                                <div class="text-xs text-blue-500 uppercase font-bold">Kilometre (TÜVTÜRK)</div>
                                <div class="text-2xl font-bold text-blue-900">{{ vehicleData.mileage.value.toLocaleString() }} KM</div>
                                <div class="text-xs text-blue-400 mt-1">Son Kontrol: {{ vehicleData.mileage.lastUpdated }}</div>
                            </div>
                            <!-- REFACTORED: Using Computed Properties -->
                            <div :class="['p-4 rounded-lg', damageBgClass]">
                                <div :class="['text-xs uppercase font-bold', damageTitleClass]">Hasar Durumu</div>
                                <div :class="['text-2xl font-bold', damageClass]">
                                    {{ damageLabel }}
                                </div>
                                <div class="text-xs mt-1 opacity-75">Sigorta Bilgi Merkezi</div>
                            </div>
                        </div>

                        <!-- Damage Records -->
                        <div v-if="vehicleData.damageStatus.hasDamage">
                            <h4 class="text-sm font-bold text-gray-500 uppercase mb-3">Hasar Geçmişi Timeline</h4>
                            <div class="space-y-3">
                                <div v-for="(rec, i) in vehicleData.damageStatus.records" :key="i" class="flex items-start">
                                    <div class="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-red-400 mr-3"></div>
                                    <div class="flex-1 bg-gray-50 p-3 rounded text-sm">
                                        <div class="flex justify-between">
                                            <span class="font-bold text-gray-800">{{ rec.date }}</span>
                                            <span class="font-bold text-red-600">{{ rec.cost }}</span>
                                        </div>
                                        <div class="text-gray-600 mt-1">
                                            {{ rec.type }} - <span class="text-gray-800">{{ rec.location }}</span> ({{ rec.severity }})
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                         <div v-else class="text-center py-6 bg-green-50 rounded border border-green-100 text-green-700">
                             🎉 Tebrikler! Bu araca ait herhangi bir kaza/hasar kaydı bulunmamaktadır.
                         </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Scoped styles if needed */
</style>
