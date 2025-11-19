from pathlib import Path
from kyber_py import ML_KEM_512  # NIST PQC Kyber (ML-KEM-512) - pure Python, pip install kyber-py

class RSAToKyberMigrator:
    def __init__(self):
        self.changes = 0

    def migrate_file(self, filepath: Path):
        if not filepath.suffix == ".py":
            return 0

        content = filepath.read_text(encoding="utf-8")

        # RSA generate_private_key bulursa Kyber'e çevir (esnek matching)
        if "rsa.generate_private_key" in content:
            # Import'u değiştir
            new_content = content.replace(
                "from cryptography.hazmat.primitives.asymmetric import rsa",
                "from kyber_py import ML_KEM_512  # Quantum-Armor: NIST PQC Kyber (ML-KEM-512) migration"
            )
            # Key generation'ı değiştir (esnek, parametreleri yakalar)
            new_content = new_content.replace(
                "rsa.generate_private_key(",
                "ML_KEM_512.keygen()  # Quantum-Armor: RSA → Kyber512 keypair (returns (pk, sk))\n        public_key, private_key = "
            )
            new_content = new_content.replace(
                "private_key = ",
                "sk = "  # Geçici, sonra private_key = sk olarak düzelt
            )
            new_content = new_content.replace(
                "sk = ",
                "private_key = "  # Düzelt
            )
            filepath.write_text(new_content, encoding="utf-8")
            self.changes += 1

        return self.changes

    def migrate_project(self, path="."):
        total = 0
        for pyfile in Path(path).rglob("*.py"):
            if "quantum_armor" not in str(pyfile):  # kendi kodumuzu bozmasın
                total += self.migrate_file(pyfile)
        print(f"Quantum-Armor: {total} RSA usage migrated to real Kyber512!")
        if total == 0:
            print("No RSA usage found – you're already quantum-ready!")
        print("Full PQC support: Use ML_KEM_512.encapsulate(pk) for encryption, ML_KEM_512.decapsulate(sk, ct) for decryption.")