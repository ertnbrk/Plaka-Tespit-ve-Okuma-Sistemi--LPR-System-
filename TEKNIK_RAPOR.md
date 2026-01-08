# Proje Teknik Raporu: Araç Plaka Tespiti ve Okuma Sistemi

**Tarih:** 08.01.2026

## 1. Proje Özeti
Bu proje, araç görüntülerinden plaka tespiti yapmak ve tespit edilen plakaları metne dönüştürmek amacıyla geliştirilmiş uçtan uca bir yapay zeka çözümüdür. Sistem, optimize edilmiş bir YOLOv8 modeli ve EasyOCR kütüphanesini FastAPI tabanlı bir web servisi üzerinde birleştirir.

## 2. Veri Seti ve Hazırlık
Modelin başarısındaki en kritik faktör, farklı kaynaklardan derlenen ve titizlikle işlenen veri setidir.

### 2.1. Veri Kaynakları
*   **Custom Dataset (Özel Veri):** Projenin başlangıcında elde olan YOLO formatındaki veri seti.
*   **Kaggle Dataset:** Çeşitliliği artırmak için eklenen, XML validasyon formatındaki harici veri seti.

### 2.2. Veri İşleme Adımları
1.  **Birleştirme (Merging):** Kaggle veri setindeki 433 görüntü ve XML etiketi, özel geliştirilen `dataset_merger.py` betiği ile işlendi.
2.  **Format Dönüşümü:** XML formatındaki bounding box koordinatları (`xmin, ymin, xmax, ymax`), YOLO formatına (`x_center, y_center, width, height`) dönüştürüldü ve normalize edildi (0-1 aralığı).
3.  **Sınıf Birliği:** Tüm verilerde sınıf ID'si `0` ('License_Plate') olarak sabitlendi.
4.  **Veri Bölme (Splitting):** Randomize edilerek şu oranlarda ayrıldı:
    *   **Eğitim (Train):** %70 (~7.384 görsel)
    *   **Doğrulama (Valid):** %20 (~2.109 görsel)
    *   **Test:** %10 (~1.056 görsel)
    *   **Toplam:** ~10.550 görsel.

## 3. Model Eğitimi

### 3.1. Model Mimarisi
*   **Temel Model:** YOLOv8 Large (`yolov8l.pt`)
*   **Neden Large?** Plakalar görüntü içinde bazen küçük alan kaplayabilir ve karmaşık arka planlara (çamur, ışık parlaması) sahip olabilir. Large model, daha fazla parametre ile bu detayları Nan veya Small modellere göre çok daha iyi öğrenir.

### 3.2. Eğitim Parametreleri
*   **Platform:** Google Colab (A100 GPU)
*   **Epochs:** 50 
*   **Batch Size:** 16 (Bellek optimizasyonu için)
*   **Optimizer:** AdamW (`lr0=0.002`)
*   **Görüntü Boyutu:** 640x640

## 4. Performans ve Karşılaştırma

Yeni "Birleştirilmiş" model, sadece Custom veri seti ile eğitilen eski modele göre ciddi performans artışı göstermiştir.

### 4.1. Metrikler
| Metrik | Eski Model (Custom Only) | Yeni Model (Kaggle+Custom) | Fark |
| :--- | :--- | :--- | :--- |
| **mAP@50** (Doğruluk) | %95.30 | **%98.46** | **+%3.16** |
| **mAP@50-95** (Hassasiyet) | %64.66 | **%72.00** | **+%7.34** |
| **Recall** (Yakalama) | %90.52 | **%96.73** | **+%6.21** |

### 4.2. Yorum
*   **Recall Artışı:** %96.7 seviyesine çıkan Recall, sistemin artık neredeyse hiçbir plakayı gözden kaçırmadığını gösterir.
*   **Hassasiyet Artışı:** mAP@50-95'teki %7'lik artış, modelin plakayı "kabaca" değil, tam sınırlarından mükemmel bir şekilde kestiğini kanıtlar. Bu, sonraki aşama olan OCR başarısını doğrudan artırır.

## 5. Gerçek Dünya Uygulaması (Pipeline)

Sistem şu adımlarla çalışır:

1.  **Girdi:** Kullanıcı bir araç fotoğrafı yükler.
2.  **Tespit (YOLOv8):** API, `best_merged_large.pt` modelini kullanarak plakanın koordinatlarını bulur. (%98 güven oranıyla)
3.  **Kırpma (Cropping):** Görüntüden sadece plaka alanı kesilir.
4.  **Ön İşleme (Preprocessing):**
    *   Gri tonlamaya çevirme (Grayscale).
    *   Görüntü büyütme (Resize 2x - OCR başarısı için kritik).
    *   Thresholding (Piksel netleştirme).
5.  **Okuma (EasyOCR):** İşlenmiş görüntüden karakterler okunur.
6.  **Temizleme (Regex):** Okunan metinden harf ve rakam dışındaki "bozuk" karakterler temizlenir.
7.  **Çıktı:** Kullanıcıya işaretlenmiş görsel ve plaka metni gösterilir.

## 6. Sonuç
Bu çalışma, doğru veri seti mühendisliği (data engineering) ve güçlü bir model mimarisi (YOLOv8-Large) birleştiğinde endüstriyel standartlarda (%98+) başarı elde edilebileceğini göstermiştir.
