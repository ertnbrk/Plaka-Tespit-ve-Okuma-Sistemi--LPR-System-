# Akıllı Şehir Plaka Tanıma Sistemi (LPR System)

Bu proje, görüntü ve videolardan otomatik plaka tanıma (ALPR), şikayet yönetimi ve admin paneli içeren kapsamlı bir web uygulamasıdır.

## 🚀 Proje Hakkında
Sistem, kullanıcıların trafik ihlallerini (hatalı park, kırmızı ışık vb.) görsel veya video ile bildirmelerine olanak tanır. Yüklenen medyalar YOLOv8 ve EasyOCR kullanılarak analiz edilir ve plakalar otomatik olarak tespit edilir. Yetkililer (Admin/Müfettiş) bu bildirimleri inceleyip onaylayabilir veya reddedebilir.

### Ana Özellikler
- **Otomatik Plaka Tanıma (LPR)**: YOLOv8 ve EasyOCR ile yüksek doğruluklu tespit.
- **Medya Analizi**: Hem resim hem de video dosyalarını işleyebilir.
- **Kullanıcı Yönetimi**: Müfettiş/Vatandaş rolleri, kayıt ve giriş (JWT Auth).
- **Şikayet Yönetimi**: Bildirim oluşturma, durumu takip etme.
- **Admin Paneli**: 
  - İstatistiksel özet (Toplam, Bekleyen, Onaylanan).
  - Gelişmiş filtreleme ve arama.
  - Kullanıcı ve şikayet detayı inceleme.
- **Modern Arayüz**: Vite + TailwindCSS ile duyarlı ve şık tasarım.

## 🛠 Teknoloji Yığını

### Backend
- **Dil**: Python 3.10+
- **Framework**: FastAPI
- **Veritabanı**: PostgreSQL (Dockerized)
- **AI/ML**: YOLOv8, EasyOCR, OpenCV
- **Araçlar**: Pydantic, SQLAlchemy, Uvicorn, Bcrypt

### Frontend
- **Framework**: Vite (Vanilla JS)
- **Stil**: TailwindCSS
- **Özellikler**: SPA benzeri yapı, Asenkron API çağrıları

## ⚙️ Kurulum ve Çalıştırma

### Gereksinimler
- Docker & Docker Compose (Veritabanı için)
- Python 3.10+
- Node.js & npm (Frontend için)

### Adım 1: Veritabanını Başlatma
Veritabanı Docker üzerinde çalışır. Backend klasöründeyken:
```powershell
# Backend klasörüne git
cd backend

# Veritabanını başlat (Arka planda)
docker-compose up -d
```

### Adım 2: Backend Kurulumu
```powershell
# Sanal ortam oluştur (Opsiyonel ama önerilir)
python -m venv venv
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını oluştur
cp .env.example .env
# .env dosyasını kendi ayarlarınızla düzenleyin (DB URL vb. varsayılanlar genelde yeterlidir)
```

### Adım 3: Uygulamayı Başlatma (Kolay Yol)
Hazırlanan PowerShell betiği veritabanını sıfırlar, örnek verileri ekler ve sunucuyu başlatır.
```powershell
./run_local.ps1
```
*Bu komut önce `seed_db.py` ile veritabanını temizleyip örnek verilerle (kullanıcılar, şikayetler) doldurur, ardından sunucuyu başlatır.*

Manuel başlatmak isterseniz:
```powershell
uvicorn main:app --reload
```

Backend şu adreste çalışacaktır: `http://localhost:8000`  
API Dokümantasyonu (Swagger): `http://127.0.0.1:8000/docs`

### Adım 4: Frontend Kurulumu
```powershell
# Frontend klasörüne git
cd ../frontend-vite

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev
```
Frontend genellikle `http://localhost:5173` adresinde açılacaktır.

## 🧪 Test Hesapları (Seed Data)

`run_local.ps1` veya `seed_db.py` çalıştırıldığında aşağıdaki hesaplar oluşturulur:

| Rol | Email | Şifre |
|---|---|---|
| **Admin** | `admin@plaka.gov.tr` | `admin123` |
| **Müfettiş** | `demo@plaka.gov.tr` | `demo123` |
| **Vatandaş** | `user1@gmail.com` | `123123` |

## 📂 Proje Yapısı

```
Finalized_Project/
├── backend/                # FastAPI Sunucusu
│   ├── app/
│   │   ├── api/            # Route handler'lar
│   │   ├── core/           # Ayarlar ve Güvenlik
│   │   ├── db/             # Veritabanı modelleri
│   │   ├── services/       # İş mantığı (LPR, Email)
│   ├── models/             # YOLO Modelleri
│   ├── run_local.ps1       # Başlatma betiği
│   └── seed_db.py          # Veritabanı tohumlama
│
├── frontend-vite/          # Vite Frontend Projesi
│   ├── js/                 # API ve Controller mantığı
│   ├── pages/              # HTML Sayfaları
│   ├── public/             # Görseller
│   └── index.html          # Giriş noktası
```

## 📝 Notlar
- **E-posta Gönderimi**: SMTP ayarları `.env` dosyasında yapılmazsa e-posta gönderimi simüle edilir (loglara yazılır).
- **Görüntü İşleme**: İlk çalıştırmada YOLO modelleri indirilebilir, bu biraz zaman alabilir.
