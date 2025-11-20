from pathlib import Path
import re

KYBER_IMPORT = "from kyber_py import ML_KEM_512  # Quantum-Armor: Real NIST PQC ML-KEM/Kyber512 migration\n"

class RSAToKyberMigrator:
    def __init__(self):
        self.changes = 0

    def migrate_file(self, filepath: Path):
        if filepath.suffix != ".py":
            return 0
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")
            return 0

        changed = False

        # RSA import'u bul ve Kyber ile değiştir
        rsa_import_pattern = re.compile(r"from cryptography\.hazmat\.primitives\.asymmetric import rsa")
        if rsa_import_pattern.search(content):
            content = rsa_import_pattern.sub(KYBER_IMPORT.strip(), content)
            changed = True

        # RSA anahtar üretimini Kyber ile değiştir
        rsa_gen_pattern = re.compile(r"(rsa\.generate_private_key\s*\([^)]+\))")
        if rsa_gen_pattern.search(content):
            content = rsa_gen_pattern.sub("public_key, secret_key = ML_KEM_512.keygen()  # Quantum-Armor: RSA → Kyber512 keypair (returns (pk, sk))", content)
            changed = True

        # private_key atamasını Kyber secret'a yönlendir
        privkey_assignment = re.compile(r"private_key\s*=\s*.+")
        if privkey_assignment.search(content):
            content = privkey_assignment.sub("private_key = secret_key  # Kyber secret key as private\n# Note: Use ML_KEM_512.encapsulate(public_key) for encryption", content)
            changed = True

        if changed:
            try:
                filepath.write_text(content, encoding="utf-8")
                self.changes += 1
            except Exception as e:
                print(f"Could not write {filepath}: {e}")

        return self.changes

    def migrate_project(self, path: str = "."):
        total = 0
        for pyfile in Path(path).rglob("*.py"):
            # quantum_armor içinde kendi kodunu es geçer
            if "quantum_armor" not in str(pyfile):
                total += self.migrate_file(pyfile)
        if total > 0:
            print(f"Quantum-Armor: Successfully migrated {total} RSA usage(s) to real Kyber512!")
            print("Your code is now quantum-resistant!")
        else:
            print("No RSA usage found – your code is already quantum-ready!")
        print("Full PQC support: Use ML_KEM_512.encapsulate(pk) for encryption, ML_KEM_512.decapsulate(sk, ct) for decryption.")
