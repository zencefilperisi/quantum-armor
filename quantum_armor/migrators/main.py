import sys
from auto_migrator import LegacyToPQC_Migrator

def select_algo():
    print("Select PQC algorithm for migration:")
    print("1: Kyber (ML-KEM) - key exchange & encryption [default]")
    print("2: Dilithium - digital signature")
    choice = input("Type 1 or 2 (or press Enter for Kyber): ").strip()
    if choice == "2":
        return "dilithium"
    return "kyber"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        migrator = LegacyToPQC_Migrator()
        migrator.rollback()
    else:
        pqc_algo = select_algo()
        migrator = LegacyToPQC_Migrator(pqc_algo=pqc_algo)
        # Dizin yolu ayarlama (bakmak istediğin ana klasörü güncelleyebilirsin)
        project_path = "../../"  # quantum_armor'ın olduğu klasörün bir üstü
        migrator.migrate_project(project_path)