# 🚗 Plaka Tespit ve Okuma Sistemi (LPR System)

Yapay zeka destekli, yüksek performanslı (**%98+ doğruluk**) otomatik plaka tanıma ve araç bilgi sorgulama sistemi.



![Recording2026-01-08211408-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/ca3483b2-9cff-4ce2-a34c-30b1f037e288)



## 🌟 Proje Hakkında

Bu proje, güvenlik kameraları veya yüklenen görsellerden araç plakalarını tespit etmek, EasyOCR ile okumak ve simüle edilmiş bir Emniyet/Tramer veritabanından araç geçmişini sorgulamak için geliştirilmiştir.

**Temel Özellikler:**
*   📸 **Görüntü Analizi:** Fotoğraflardan anlık plaka tespiti.
*   🎥 **Video Analizi:** Videolardan araç takibi (Tracking) ve plaka okuma.
*   🔍 **Akıllı OCR:** Hatalı karakterleri regex ile düzelten akıllı okuma motoru.
*   🚓 **Simüle Araç Sorgusu:** Plaka üzerinden hasar kaydı, KM ve araç detaylarını getiren simülasyon servisi.
*   ⚡ **Modern Frontend:** Vite + Vue 3 ile geliştirilmiş reaktif arayüz.
*   🚀 **FastAPI Backend:** Yüksek performanslı asenkron API.

## 📊 Performans Ölçümleri

Proje, **YOLOv8 Large** modeli kullanılarak eğitilmiştir. Özel ve Kaggle veri setlerinin birleştirilmesiyle (%70 Eğitim, %20 Doğrulama, %10 Test) eğitilen modelin sonuçları:

| Metrik | Değer | Açıklama |
| :--- | :--- | :--- |
| **mAP@50** | **%98.46** | Modelin plaka tespit kesinliği |
| **mAP@50-95** | **%72.00** | Kutu hassasiyeti (Perfect bounding box) |
| **Recall** | **%96.73** | Plakaları gözden kaçırmama oranı |

<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/a8bc074d-f0a4-4d41-bece-f8b426cd4e1c" />


> **Not:** Model, karlı, çamurlu ve açılı plakalarda bile yüksek başarı göstermektedir.

## 🛠️ Teknolojiler

*   **Backend:** Python, FastAPI, YOLOv8, EasyOCR, Pydantic
*   **Frontend:** Vue.js 3, Vite, Tailwind CSS, SweetAlert2
*   **Veri İşleme:** OpenCV, Pandas, NumPy

## 🚀 Kurulum

Projeyi çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
*   Python 3.10+
*   Node.js 18+

### 1. Backend Kurulumu

```bash
cd backend
# Sanal ortam oluşturun (Opsiyonel)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Servisi Başlatın
uvicorn main:app --reload
```
*Backend `http://localhost:8000` adresinde çalışacaktır.*

### 2. Frontend Kurulumu

```bash
cd frontend
# Bağımlılıkları yükleyin
npm install

# Uygulamayı Başlatın
npm run dev
```
*Frontend `http://localhost:5173` adresinde açılacaktır.*

## 📂 Klasör Yapısı

```
Finalized_Project/
├── backend/            # FastAPI servis kodları ve AI modelleri
│   ├── main.py         # API Endpoints
│   ├── inference.py    # Resim işleme mantığı
│   ├── models/         # Eğitilmiş .pt dosyaları
│   └── mock_db.py      # Simüle edilmiş araç veritabanı
├── frontend/           # Vue 3 + Vite Projesi
│   ├── src/            # Vue bileşenleri
│   └── index.html      # Giriş noktası
└── TEKNIK_RAPOR.md     # Detaylı teknik dökümantasyon
```

## 🛡️ Lisans
Bu proje eğitim ve test amaçlı geliştirilmiştir.
