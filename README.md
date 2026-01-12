# 📄 Word to PDF Dönüştürücü

Windows uygulaması - Word (.docx) dosyalarını PDF formatına hızlıca dönüştürün!

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)

## ✨ Özellikler

- 🎯 **Basit Arayüz** - Kolay ve anlaşılır kullanım
- ⚡ **Hızlı Dönüştürme** - Saniyeler içinde PDF oluştur
- 🖼️ **Resim Desteği** - Tüm görseller korunur
- 📋 **Tablo Desteği** - Tablolar düzgün şekilde aktarılır
- 🌍 **Çoklu Dil** - Türkçe, Rusça, Arapça vb. karakterler
- 💾 **Otomatik Kayıt** - İndirilmiş Dosyalar klasörüne kaydedilir
- 📂 **Dosya Yönetimi** - Aynı isimde dosya varsa otomatik numalandırma

## 🚀 Hızlı Başlangıç

### Gereksinimler

- **Python** 3.8 veya üzeri
- **Windows** 7 veya üzeri
- **LibreOffice** (Dönüştürme için gerekli)

### LibreOffice Kurulumu

1. https://www.libreoffice.org/download/ adresine gidin
2. Windows için installer indirin
3. Kurulumu tamamlayın
4. Uygulamayı başlatın

### Adım 1: Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/kayaal34/world-pdf-converter.git
cd world-pdf-converter

# Python bağımlılıklarını kurun
pip install -r requirements.txt
```

### Adım 2: Çalıştırma

```bash
python run.py
```

## 📖 Kullanım

1. **Dosya Seçin**
   - "Word Dosyası Seç (.docx)" butonuna tıklayın
   - Dönüştürmek istediğiniz Word dosyasını seçin

2. **Dönüştürün**
   - "PDF'ye Dönüştür" butonuna tıklayın
   - Dönüştürme işlemi başlayacak

3. **İndirin**
   - PDF dosyası otomatik olarak **İndirilmiş Dosyalar** klasörüne kaydedilir
   - Dosyayı açmak isteyip istemediğinizi soracak

## 📁 Proje Yapısı

```
world-pdf-converter/
├── run.py                    # Ana uygulama giriş noktası
├── requirements.txt          # Python bağımlılıkları
├── README.md                # Dokümantasyon
├── src/
│   ├── converter.py         # PDF dönüştürme motoru
│   └── gui.py              # Grafik kullanıcı arayüzü (Tkinter)
├── .vscode/
│   └── settings.json       # VS Code ayarları
└── .github/
    └── copilot-instructions.md
```

## 🔧 Teknik Detaylar

### Teknoloji Stack

| Kütüphane | Versiyon | Kullanım |
|-----------|----------|---------|
| Python | 3.8+ | Programlama dili |
| Tkinter | Built-in | GUI Framework |
| docx2pdf | 0.1.8 | DOCX → PDF dönüştürme |
| python-docx | 0.8.11 | Word dosyası işleme |
| LibreOffice | Kurulu | Dönüştürme backend'i |

### Dönüştürme Süreci

1. Word dosyası (`.docx`) seçilir
2. `docx2pdf` kütüphanesi kullanarak LibreOffice'e gönderilir
3. LibreOffice dosyayı PDF formatına dönüştürür
4. PDF dosyası İndirilmiş Dosyalar klasörüne kaydedilir

## 🐛 Sorun Giderme

### "LibreOffice bulunamadı" hatası

**Çözüm:** LibreOffice'i kurun
```bash
# https://www.libreoffice.org/download/
```

### Dönüştürme başarısız oluyor

1. Dosyanın `.docx` formatında olduğundan emin olun
2. Dosyayı başka bir programda kapalı tutun
3. Dosyayı yeniden kaydedin
4. Uygulamayı yeniden başlatın

### Karakterler yanlış görünüyor

- LibreOffice'in en son sürümünü kurun
- Uygulamayı yeniden başlatın

## 📝 Örnek Kullanım

```python
from src.converter import WordToPDFConverter

# Converter'ı oluştur
converter = WordToPDFConverter()

# DOCX dosyasını PDF'ye dönüştür
success = converter.convert(
    'input.docx',
    'output.pdf'
)

if success:
    print("✓ Dönüştürme başarılı!")
else:
    print("✗ Dönüştürme başarısız!")
```

## 📊 Desteklenen Formatlar

| Format | Giriş | Çıkış | Açıklama |
|--------|-------|-------|----------|
| DOCX | ✅ | - | Microsoft Word |
| PDF | - | ✅ | Taşınabilir belge |
| Resimler | ✅ | ✅ | JPEG, PNG, BMP vb. |
| Tablolar | ✅ | ✅ | Kompleks tablolar |

## 🤝 Katkı Sağlama

Pull requestler hoş karşılanır! Büyük değişiklikler için lütfen bir issue açarak tartışın.

## 📄 Lisans

Bu proje MIT Lisansı altında yayınlanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

- **Yahya Kaya** - [@kayaal34](https://github.com/kayaal34)

## 💬 İletişim & Destek

- **GitHub Issues**: Hataları raporlayın ve önerilerinizi paylaşın
- **Tartışmalar**: Soru ve fikirler için GitHub Discussions'ı kullanın

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

**Son Güncelleme:** 12 Ocak 2026

