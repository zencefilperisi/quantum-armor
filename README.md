<p align="center">
  <h1 align="center">Quantum-Armor</h1>
</p>

<p align="center">
  <a href="https://github.com/zencefilperisi/quantum-armor/stargazers">
    <img src="https://img.shields.io/github/stars/zencefilperisi/quantum-armor?style=social" alt="Stars"/>
  </a>
  <img src="https://img.shields.io/pypi/v/quantum-armor?color=success&label=pypi" alt="PyPI"/>
  <img src="https://img.shields.io/github/license/zencefilperisi/quantum-armor?color=blue" alt="License"/>
  <br><br>
  <strong>Tek tıklamayla kuantum sonrası kriptografi denetim aracı</strong><br>
  Hatta pip, requests ve click paketlerinin içinde bile 23 kuantum açığı buldu!
</p>

---

## 🚀 Neden Quantum-Armor?

- 2030’a kadar RSA ve ECC kırılacak → geçiş bugün başlıyor  
- Sıfır yapılandırma, her Python projesinde anında çalışır  
- RSA, ECC, DH kullanımını algılar (hatta kendi venv’inde bile!)  
- NIST onaylı PQC alternatiflerini önerir (Kyber, Dilithium, Falcon)

---

## 📦 Kurulum

```bash
pip install quantum-armor
```
## Kullanım
```bash
quantum-armor scan /path/to/your/project
## veya bulunduğun dizini taramak için
quantum-armor scan .
```

<p align="center"> ⭐ Star this repo if you're preparing for the quantum apocalypse! ⭐ </p>

## İlk Test Sonuçları

İlk testte kendi bağımlılıklarını taradı → pip, requests, click, urllib3 gibi paketlerde
23 tane kuantumla kırılabilir kriptografik kullanım tespit etti!

## Desteklenen Geçişler
```bash
Klasik       → PQC Alternatifi        Durum
RSA          CRYSTALS-Kyber           NIST Onaylı
ECC/ECDSA    CRYSTALS-Dilithium       NIST Onaylı
DH           CRYSTALS-Kyber/NTRU      Önerilen
```
<p align="center"> Made with ❤️ by @zencefilperisi </p> ```
