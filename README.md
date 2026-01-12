# 🚗 Plaka Tespit ve Okuma Sistemi (LPR System)

Yapay zeka destekli, yüksek performanslı otomatik plaka tanıma, ihlal tespiti ve şikayet yönetim sistemi.

![System Preview](https://github.com/user-attachments/assets/ca3483b2-9cff-4ce2-a34c-30b1f037e288)

## 🌟 Proje Hakkında

Bu proje, şehir güvenliği kameraları veya kullanıcılar tarafından yüklenen görsellerden araç plakalarını tespit etmek, EasyOCR ve YOLOv8 ile okumak ve bunları bir yönetim panelinde raporlamak için geliştirilmiştir. Sistem, vatandaşların ihlal bildirimi yapmasına ve yetkililerin bu bildirimleri incelemesine olanak tanır.

**Temel Özellikler:**
*   📸 **LPR (Plaka Tanıma):** YOLOv8 ve EasyOCR ile yüksek doğruluklu plaka tespiti ve okuma.
*   🎥 **Medya Analizi:** Hem resim hem de video dosyalarını işleyebilme.
*   🚦 **İhlal Yönetimi:** Hatalı park, kırmızı ışık vb. ihlallerin bildirimi.
*   👮 **Yönetim Paneli:** Müfettişler için gelişmiş dashboard, filtreleme ve istatistikler.
*   🔒 **Güvenlik:** JWT tabanlı kimlik doğrulama ve rol yönetimi (Admin/Müfettiş/Kullanıcı).
*   ⚡ **Modern Frontend:** Vanilla JS + Tailwind CSS ile hafif ve hızlı arayüz.
*   🚀 **FastAPI Backend:** Yüksek performanslı, asenkron ve ölçeklenebilir altyapı.

## 🛠️ Teknolojiler

*   **Backend:** Python 3.10+, FastAPI, SQLAlchemy, Pydantic
*   **AI/ML:** YOLOv8, EasyOCR, OpenCV
*   **Veritabanı:** PostgreSQL (Docker)
*   **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (CDN)
*   **DevOps:** Docker, Docker Compose

## 🚀 Hızlı Başlangıç (Quick Start)

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
*   Docker & Docker Compose (Veritabanı için)
*   Python 3.10+

### 1. Veritabanını Başlatma
Veritabanı servisini Docker kullanarak başlatın:
```bash
cd backend
docker-compose up -d
```

### 2. Backend Kurulumu ve Başlatma
Backend servisini kurun, veritabanını hazırlayın ve başlatın.

**Otomatik Kurulum (Önerilen - Windows Powershell):**
```powershell
# Backend klasöründe
./run_local.ps1
```
*Bu komut gerekli tabloları oluşturur, örnek verileri (admin kullanıcısı vb.) ekler ve sunucuyu başlatır.*

**Manuel Kurulum:**
```bash
# Sanal ortam oluşturup aktif edin
python -m venv venv
.\venv\Scripts\activate  # Mac/Linux: source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Veritabanını sıfırla ve örnek verileri yükle
python seed_db.py

# Sunucuyu başlat
uvicorn main:app --reload
```
API Adresi: `http://localhost:8000`  
Dokümantasyon: `http://localhost:8000/docs`

### 3. Frontend Çalıştırma
Frontend projesi statik HTML/JS yapısındadır, herhangi bir derleme (build) işlemine gerek yoktur.

1.  `frontend-vite/pages/login.html` dosyasını tarayıcınızda açın.
2.  VEYA (Önerilen) bir statik sunucu kullanın:
    ```bash
    cd frontend-vite
    npx serve .
    # veya
    python -m http.server 5500
    ```
    Tarayıcıda `http://localhost:5500` adresine gidin.

## 🧪 Test Hesapları

Sistemde tanımlı varsayılan kullanıcılar:

| Rol | Email | Şifre |
|---|---|---|
| **Admin** | `admin@plaka.gov.tr` | `admin123` |
| **Müfettiş** | `demo@plaka.gov.tr` | `demo123` |
| **Kullanıcı** | `user1@gmail.com` | `123123` |

## 📂 Klasör Yapısı

```
Finalized_Project/
├── backend/                # FastAPI Backend
│   ├── app/                # Uygulama kodları (API, Auth, Services)
│   ├── models/             # YOLO ağırlık dosyaları (.pt)
│   └── seed_db.py          # Veritabanı tohumlama betiği
│
├── frontend-vite/          # Frontend (Statik)
│   ├── pages/              # HTML sayfaları (login, dashboard, admin...)
│   ├── js/                 # JavaScript mantığı (API, Auth, UI...)
│   └── public/             # Görseller ve ikonlar
```

## 🛡️ Lisans
Bu proje eğitim ve test amaçlı geliştirilmiştir.
