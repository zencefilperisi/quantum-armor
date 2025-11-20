# Quantum Armor

Quantum Armor, klasik şifreleme algoritmalarını (RSA, ECC, DSA, DH gibi) tek komutla, NIST onaylı kuantum-dirençli kriptografiye (Kyber/ML-KEM veya Dilithium) **otomatik** olarak dönüştüren bir migrasyon aracıdır. Legacy Python (& JS) projeleriniz, Quantum Armor ile kodunuzu manuel güncellemeden bir anda geleceğe uyumlu hale gelir.

---

## 🚀 Özellikler (2025 Güncel Sürüm!)

- **Çoklu Algoritma Desteği:**  
  Klasik RSA, ECC, DSA ve DH key generation kodlarını yakalayıp PQC’ye dönüştürür.
- **Kullanıcı Seçimli PQC (Komut Satırı veya GUI):**  
  Otomatik veya interaktif olarak Kyber (ML-KEM), Dilithium gibi algoritma seçimi ile migrasyon.
- **Otomatik Migre & JSON Raporlama:**  
  Migrasyon sonrası dosya değişiklikleri ve yeni algoritmalar JSON raporu olarak saklanır.
- **Rollback (Geri Al) Özelliği:**  
  Her değişimden önce otomatik dosya yedeği alınır. Tek komutla tüm dosyaları eski haline döndürebilirsin.
- **Test Scripti ile Kontrol:**  
  Migrasyon sonrası dosyaların PQC uyumlu ve doğru güncellenip güncellenmediği otomatik test edilir.
- **Multi-Language Demo:**  
  Python dışında, örnek JavaScript dosyaları için de RSA → Kyber/Dilithium dönüşüm desteği.
- **Basit Web Arayüzü (Flask GUI):**  
  Proje dizinini ve algoritmayı seçip kod migrasyonunu web üzerinden gerçekleştirebilirsin.
- **Kolay Entegrasyon:**  
  CLI ve GUI ile projelerde anında kullanılabilir ve genişletilebilir.

---

## 🔧 Kurulum

```bash
pip install kyber-py dilithium-py flask
```

---

## ⚡ Hızlı Kullanım (CLI)

```bash
python quantum_armor/migrators/main.py
```
- Size algoritma sorar: Kyber veya Dilithium seçin.
- Otomatik migrasyon başlar: Tüm projede klasik anahtar üretimi PQC ile değişir.
- Detaylar `migration_report.json` dosyasına kaydedilir.

**Rollback:**
```bash
python quantum_armor/migrators/main.py rollback
```
Değişen dosyalar eski haline döner.

---

## 🌐 Web GUI
```bash
python quantum_armor/migrators/web_gui.py
```
- Tarayıcıdan (`localhost:5000`) projeni ve algoritmayı seç, migrasyonu başlat.

---

## 🧪 Test Scripti
Migrasyonun başarıyla gerçekleşip gerçekleşmediğini otomatik kontrol eder:
```bash
python quantum_armor/migrators/test_migration.py
```

---

## 🕹️ JavaScript Demo
`js_migrator_demo.js` ile JS kodlarında da legacy → PQC dönüşümü örneği.

---

## 📚 Sonuç

Artık projen kuantum direncine hazır!  
Quantum Armor ile kodun hem güvenli, hem de geleceğin kriptografisine uyumlu.

👉 Daha fazla örnek ve dokümantasyon için:  
- [Web Arayüzü](#web-gui)
- [Rollback](#rollback)
- [Test Scripti](#test-scripti)
- [Multi-language Demo](#multi-language-demo)

---

## 👩‍💻 Katkı ve Destek

Her türlü iyileştirme, yeni algoritma ekleme ve PR’a açık!  
Soruların için: [issues sekmesine](https://github.com/zencefilperisi/quantum-armor/issues) bakabilirsin.

---

_Tüm NIST onaylı algoritma kütüphaneleri ve modern best-practices ile uyumludur.  
Quantum Armor, legacy kodun geleceğe taşınmasında lider bir çözümdür._