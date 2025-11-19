import ast
from pathlib import Path

# Klasik algoritmalar ve PQC karşılıkları
VULNERABLE_PATTERNS = {
    "RSA": ["rsa", "RSA", "pkcs1", "PKCS1", "generate_rsa", "RSA.import_key"],
    "ECC": ["ecc", "ECC", "ecdsa", "ECDSA", "EllipticCurve", "ec."],
    "DH":  ["DiffieHellman", "DH", "diffie-hellman"],
}

PQC_REPLACEMENTS = {
    "RSA": "CRYSTALS-Kyber",
    "ECC": "CRYSTALS-Dilithium",
    "DH":  "CRYSTALS-Kyber or NTRU",
}

def scan_file(filepath: Path):
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
    except Exception:
        # Parse edilemezse string bazlı basit arama
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read().lower()
        for algo, keywords in VULNERABLE_PATTERNS.items():
            for kw in keywords:
                if kw.lower() in source:
                    findings.append({"algo": algo, "replacement": PQC_REPLACEMENTS[algo], "line": "?"})
        return findings

    # AST ile akıllı tarama
    for node in ast.walk(tree):
        # Import kontrolü
        if isinstance(node, ast.Import):
            for name in node.names:
                for algo, keywords in VULNERABLE_PATTERNS.items():
                    if any(kw.lower() in name.name.lower() for kw in keywords):
                        findings.append({"algo": algo, "replacement": PQC_REPLACEMENTS[algo], "line": node.lineno})
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for algo, keywords in VULNERABLE_PATTERNS.items():
                if any(kw.lower() in module.lower() for kw in keywords):
                    findings.append({"algo": algo, "replacement": PQC_REPLACEMENTS[algo], "line": node.lineno})

        # Fonksiyon çağrısı kontrolü
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id"):
                func_name = node.func.id
                for algo, keywords in VULNERABLE_PATTERNS.items():
                    if any(kw.lower() in func_name.lower() for kw in keywords):
                        findings.append({"algo": algo, "replacement": PQC_REPLACEMENTS[algo], "line": node.lineno})

    return findings

def scan_directory(path: str = "."):
    path = Path(path)
    results = {}
    for py_file in path.rglob("*.py"):
        if findings := scan_file(py_file):
            results[str(py_file)] = findings
    return results