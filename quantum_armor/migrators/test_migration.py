import json
import os

def test_migration(report_path="migration_report.json"):
    if not os.path.exists(report_path):
        print(f"Test failed: No report file {report_path}")
        return

    with open(report_path, "r", encoding="utf-8") as fp:
        report = json.load(fp)

    success = True
    for entry in report:
        if not entry["changes"]:
            print(f"Test failed: No changes reported for {entry['file']}")
            success = False
        else:
            print(f"[OK] {entry['file']} migrated. Detail: {entry['changes']}")
            # Ek kontrol: Dosyada PQC import var mı?
            with open(entry["file"], "r", encoding="utf-8") as fsrc:
                content = fsrc.read()
                pqc_import_found = (entry["pqc_algo"].lower() in content.lower())
                if not pqc_import_found:
                    print(f"Test failed: PQC import not found in {entry['file']}")
                    success = False

    if success:
        print("✔ All migrations passed assertions")
    else:
        print("❌ Some migrations failed. See above.")

if __name__ == "__main__":
    test_migration()