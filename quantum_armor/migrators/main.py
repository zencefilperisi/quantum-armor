# quantum_armor/migrators/main.py
try:
    import astunparse
except ImportError:
    from astunparse import unparse as astunparse_unparse
    astunparse = type('obj', (object,), {'unparse': astunparse_unparse})
import argparse
import ast
from pathlib import Path
from .backup import create_backup, list_backups, rollback
from .ast_parser import scan_directory_ast
from .replacer import PQCMigrator  # yarın tamamlanacak
import astunparse

def migrate_project(path: str, algo: str = "kyber"):
    path = Path(path).resolve()
    if not path.exists():
        print(f"[ERROR] Path not found: {path}")
        return

    print(f"[SCAN] Scanning {path} for legacy cryptography...")
    results = scan_directory_ast(str(path))

    if not results:
        print("[OK] No legacy crypto found. Already quantum-resistant!")
        return

    files = list(results.keys())
    print(f"[FOUND] {len(files)} files with legacy crypto usage.")

    # 1. Backup
    print("[BACKUP] Creating secure backup...")
    backup_tag = create_backup(files)
    print(f"[BACKUP] Backup saved: {backup_tag}")

    # 2. Migrate
    migrated = 0
    for file_path in files:
        fp = Path(file_path)
        try:
            source = fp.read_text(encoding="utf-8")
            tree = ast.parse(source)
            migrator = PQCMigrator(algo=algo)  # yarın burası aktif olacak
            new_tree = migrator.visit(tree)

            if migrator.changes_made:
                new_code = astunparse.unparse(new_tree)
                fp.write_text(new_code, encoding="utf-8")
                print(f"[MIGRATED] {file_path}")
                migrated += 1
            else:
                print(f"[SKIPPED] No changes needed: {file_path}")
        except Exception as e:
            print(f"[ERROR] Failed {file_path}: {e}")

    print(f"\n[COMPLETE] Migration finished.")
    print(f"   Migrated files: {migrated}")
    print(f"   Backup tag: {backup_tag}")
    print(f"   Rollback command: python -m quantum_armor.migrators.main --rollback {backup_tag}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantum Armor – Automated PQC Migration")
    parser.add_argument("path", nargs="?", default=".", help="Project directory (default: current)")
    parser.add_argument("--algo", choices=["kyber", "dilithium"], default="kyber", help="PQC algorithm")
    parser.add_argument("--rollback", type=str, help="Rollback to backup tag")

    args = parser.parse_args()

    if args.rollback:
        print(f"[ROLLBACK] Restoring from backup {args.rollback}...")
        restored = rollback(args.rollback)
        print(f"[ROLLBACK] Restored {len(restored)} files.")
    else:
        migrate_project(args.path, args.algo)