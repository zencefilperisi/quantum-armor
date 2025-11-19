# Quantum-Armor 🛡️

[![PyPI version](https://badge.fury.io/py/quantum-armor.svg)](https://badge.fury.io/py/quantum-armor)
[![Stars](https://img.shields.io/github/stars/zencefilperisi/quantum-armor)](https://github.com/zencefilperisi/quantum-armor/stars)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**One-click post-quantum cryptography audit & migration tool.**  
Scan your codebase for vulnerable crypto (RSA, ECC) and get instant migration paths to NIST-approved PQC algorithms like Kyber, Dilithium, and Falcon.

## Why Quantum-Armor?
- **Quantum threats are real**: By 2030, quantum computers will break classical crypto. Start migrating *now*.
- **Dead simple**: `pip install quantum-armor && quantum-armor scan .` – that's it.
- **Zero config**: Works on Python, JS, Go projects out-of-the-box.

![Demo GIF Placeholder](https://via.placeholder.com/800x400?text=Scanning+Your+Code...+PQC+Recommendations)  
*(GIF bu akşam eklenecek – CLI demo'su çalışırken)*

## Quick Start
```bash
pip install quantum-armor
quantum-armor scan /path/to/your/project
