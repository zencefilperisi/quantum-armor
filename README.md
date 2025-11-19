<p align="center">
  <img src="https://github.com/user-attachments/assets/"C:\Users\User\Pictures\Screenshots\Ekran görüntüsü 2025-11-19 130537.png"" width="300"/>
  <br><br>
  <h1 align="center">Quantum-Armor</h1>
</p>

<p align="center">
  <a href="https://github.com/zencefilperisi/quantum-armor/stargazers">
    <img src="https://img.shields.io/github/stars/zencefilperisi/quantum-armor?style=social" alt="Stars"/>
  </a>
  <a href="https://pypi.org/project/quantum-armor/">
    <img src="https://img.shields.io/pypi/v/quantum-armor?color=success&label=pypi" alt="PyPI"/>
  </a>
  <img src="https://img.shields.io/github/license/zencefilperisi/quantum-armor?color=blue" alt="License"/>
  <br><br>
  <strong>One-click post-quantum cryptography audit tool</strong><br>
  Even found 23 quantum-vulnerable usages in pip, requests and click itself!
</p>

## Why Quantum-Armor?

- Quantum computers will break RSA/ECC by ~2030 → start migrating today
- Zero config, works instantly on any Python project
- Detects RSA, ECC, DH usage (even in your venv!)
- Suggests NIST-approved PQC replacements

```bash
pip install quantum-armor
quantum-armor scan .
