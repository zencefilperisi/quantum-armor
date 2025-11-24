# Güvenli backup / manifest / rollback mekanizması
from pathlib import Path
import shutil
import hashlib
import json
from datetime import datetime

BACKUP_ROOT = Path(__file__).parent / "backups"

def _sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def create_backup(files: list, tag: str = None):
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    ts = tag or datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dest = BACKUP_ROOT / ts
    dest.mkdir(parents=True, exist_ok=False)
    manifest = {'created_at': ts, 'files': []}
    for f in files:
        p = Path(f)
        if not p.exists():
            continue
        rel = p.name
        dst = dest / rel
        shutil.copy2(p, dst)
        manifest['files'].append({
            'original_path': str(p.resolve()),
            'backup_path': str(dst.resolve()),
            'sha256': _sha256_file(dst),
            'size': dst.stat().st_size
        })
    manifest_path = dest / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest_path

def list_backups():
    return sorted([d.name for d in BACKUP_ROOT.iterdir() if d.is_dir()])

def rollback(backup_tag: str):
    src = BACKUP_ROOT / backup_tag
    manifest_path = src / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError("Manifest not found for backup: " + backup_tag)
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    restored = []
    for entry in manifest['files']:
        bpath = Path(entry['backup_path'])
        if not bpath.exists():
            raise FileNotFoundError(f"Backup entry missing: {bpath}")
        if _sha256_file(bpath) != entry['sha256']:
            raise ValueError(f"Checksum mismatch for backup file {bpath}; aborting rollback.")
        orig = Path(entry['original_path'])
        orig.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bpath, orig)
        restored.append(str(orig))
    return restored