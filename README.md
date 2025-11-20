# Quantum Armor

Quantum Armor is a migration tool that automatically converts legacy cryptographic code (RSA, ECC, DSA, DH, etc.) to NIST-approved quantum-resistant algorithms (Kyber/ML-KEM or Dilithium) with a single command. With Quantum Armor, your Python (& JS) projects become future-proof without manual code updates—just migrate and go!

---

## Features

- **Multi-Algorithm Support:**  
  Finds and migrates legacy key generation code for RSA, ECC, DSA, and DH to post-quantum cryptography (PQC).
- **User-Selectable PQC Algorithms (CLI & GUI):**  
  Choose Kyber (ML-KEM), Dilithium, or others interactively for migration.
- **Automatic Migration & JSON Reporting:**  
  Every change is reported and documented in a JSON migration report.
- **Rollback (Backup/Restore):**  
  Automatically backs up files before migration; revert to originals with a single command.
- **Migration Test Script:**  
  Automatically tests and validates successful migration and PQC compliance.
- **Multi-Language Demo:**  
  Python and JavaScript support—see examples for legacy → PQC transformation in both.
- **Simple Web GUI (Flask):**  
  Migrate your project from a user-friendly web interface.
- **Easy Integration:**  
  Use from the command line or integrate as a module for your custom automations.

---

## Installation

```bash
pip install kyber-py dilithium-py flask
```

---

## Quick Usage (CLI)

```bash
python quantum_armor/migrators/main.py
```
- Choose your preferred PQC algorithm: Kyber or Dilithium.
- Automatically migrates all legacy cryptography code in your project.
- Detailed changes are logged to `migration_report.json`.

**Rollback:**
```bash
python quantum_armor/migrators/main.py rollback
```
Restores all changed files from backups.

---

## Web GUI

```bash
python quantum_armor/migrators/web_gui.py
```
- Open your browser at `localhost:5000`.
- Select project path and PQC algorithm, and start migration from the web interface.

---

## Test Script

Automatically checks and validates migrated code:
```bash
python quantum_armor/migrators/test_migration.py
```

---

## JavaScript Demo

Use `js_migrator_demo.js` to migrate legacy JS cryptography code to PQC.

---

## Summary

Your project is now quantum-resistant!  
With Quantum Armor, your code is secure against the threats of future quantum computers, and ready for adoption in any modern cryptographic workflow.

For more examples and documentation:
- [Web GUI](#web-gui)
- [Rollback](#rollback)
- [Test Script](#test-script)
- [Multi-language Demo](#multi-language-demo)

---

## Contribution & Support

Contributions, improvements, and new algorithms are welcome!  
For questions, see [issues page](https://github.com/zencefilperisi/quantum-armor/issues).

---

_All algorithms are NIST-compliant. Quantum Armor is the leading tool for future-proofing your legacy cryptography code._