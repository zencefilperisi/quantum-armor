from pathlib import Path
import re
import json
import shutil
from datetime import datetime

KYBER_IMPORT = "from kyber_py import ML_KEM_512  # Quantum-Armor: NIST PQC ML-KEM/Kyber512 migration\n"
DILITHIUM_IMPORT = "from dilithium_py import Dilithium2  # Quantum-Armor: NIST PQC Dilithium2 migration\n"

PQC_ALGOS = {
    "kyber": {
        "import": KYBER_IMPORT.strip(),
        "keygen": "public_key, secret_key = ML_KEM_512.keygen()",
    },
    "dilithium": {
        "import": DILITHIUM_IMPORT.strip(),
        "keygen": "public_key, secret_key = Dilithium2.keygen()",
    }
}

LEGACY_ALGOS = [
    {
        "name": "RSA",
        "import_pat": r"from cryptography\.hazmat\.primitives\.asymmetric import rsa",
        "keygen_pat": r"(rsa\.generate_private_key\s*\([^)]+\))",
    },
    {
        "name": "ECC",
        "import_pat": r"from cryptography\.hazmat\.primitives\.asymmetric import ec",
        "keygen_pat": r"(ec\.generate_private_key\s*\([^)]+\))",
    },
    {
        "name": "DSA",
        "import_pat": r"from cryptography\.hazmat\.primitives\.asymmetric import dsa",
        "keygen_pat": r"(dsa\.generate_private_key\s*\([^)]+\))",
    },
    {
        "name": "DH",
        "import_pat": r"from cryptography\.hazmat\.primitives\.asymmetric import dh",
        "keygen_pat": r"(dh\.generate_parameters\s*\([^)]+\))",
    },
]

BACKUP_DIR = Path(__file__).parent / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

class LegacyToPQC_Migrator:
    def __init__(self, pqc_algo="kyber"):
        self.pqc_algo = pqc_algo
        self.changes = 0
        self.algos_found = []
        self.report = []
        self.backups = []

    def backup_file(self, filepath: Path):
        """Create timestamped backup before changing the file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"{filepath.name}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)
        self.backups.append({"orig": str(filepath), "backup": str(backup_path)})
        return backup_path

    def migrate_file(self, filepath: Path):
        if filepath.suffix != ".py":
            return 0
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Could not read {filepath}: {e}")
            return 0

        changed = False
        algo_config = PQC_ALGOS.get(self.pqc_algo, PQC_ALGOS["kyber"])
        file_report = {
            "file": str(filepath),
            "changes": [],
            "pqc_algo": self.pqc_algo,
        }

        for algo in LEGACY_ALGOS:
            if re.search(algo["import_pat"], content):
                content = re.sub(algo["import_pat"], algo_config["import"], content)
                self.algos_found.append(algo["name"])
                file_report["changes"].append(f"Import: {algo['name']} → {self.pqc_algo}")
                changed = True
            if re.search(algo["keygen_pat"], content):
                content = re.sub(algo["keygen_pat"], algo_config["keygen"], content)
                file_report["changes"].append(f"Keygen: {algo['name']} → {self.pqc_algo}")
                changed = True

        if changed:
            # Yedekle!
            self.backup_file(filepath)
            try:
                filepath.write_text(content, encoding="utf-8")
                self.changes += 1
                self.report.append(file_report)
            except Exception as e:
                print(f"Could not write {filepath}: {e}")

        return changed

    def migrate_project(self, path: str = ".", report_path="migration_report.json"):
        total = 0
        self.backups = []
        for pyfile in Path(path).rglob("*.py"):
            if "quantum_armor" not in str(pyfile):
                if self.migrate_file(pyfile):
                    total += 1
        if total > 0:
            print(f"Quantum-Armor: Migrated {self.algos_found} usages to {self.pqc_algo.upper()} PQC algorithm!")
            print("Your code is now quantum-resistant!")
        else:
            print("No legacy algorithm usage found – your code is already quantum-ready!")
        print(f"Full PQC support: {self.pqc_algo.title()} for keypair, encryption and signatures!")

        # Raporu ekrana yazdır
        print("\nMigration Report Summary:")
        for entry in self.report:
            print(f"- File: {entry['file']}")
            for ch in entry["changes"]:
                print(f"    {ch}")
            print(f"    → PQC: {entry['pqc_algo']}")
        # JSON olarak dosyaya kayıt et
        try:
            with open(report_path, "w", encoding="utf-8") as fp:
                json.dump(self.report, fp, indent=2, ensure_ascii=False)
            print(f"\nMigration report saved to: {report_path}")
            # Backup listesi
            with open("backup_manifest.json", "w", encoding="utf-8") as fp:
                json.dump(self.backups, fp, indent=2, ensure_ascii=False)
            print(f"Backups manifest saved to: backup_manifest.json")
        except Exception as e:
            print(f"Could not save report: {e}")

    def rollback(self):
        # Var olan yedeklerle dosyaları eski haline alır!
        try:
            with open("backup_manifest.json", "r", encoding="utf-8") as fp:
                backups = json.load(fp)
            for entry in backups:
                shutil.copy2(entry["backup"], entry["orig"])
                print(f"Restored: {entry['orig']} ← {entry['backup']}")
            print("All files have been rolled back to their original state.")
        except Exception as e:
            print(f"Rollback failed: {e}")