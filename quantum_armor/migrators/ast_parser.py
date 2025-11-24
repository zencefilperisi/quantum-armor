# AST tabanlı import / keygen / kullanım tespiti
from pathlib import Path
import ast
from typing import List, Dict, Any

class CryptoUsageVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.calls = []

    def visit_Import(self, node: ast.Import):
        for n in node.names:
            self.imports.append({'module': n.name, 'name': None, 'lineno': node.lineno})
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        mod = node.module or ""
        for n in node.names:
            self.imports.append({'module': mod, 'name': n.name, 'lineno': node.lineno})
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        func_name = self._get_full_name(node.func)
        self.calls.append({'func': func_name, 'lineno': node.lineno, 'node': node})
        self.generic_visit(node)

    def _get_full_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            parts = []
            cur = node
            while isinstance(cur, ast.Attribute):
                parts.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                parts.append(cur.id)
            parts.reverse()
            return ".".join(parts)
        elif isinstance(node, ast.Call):
            return self._get_full_name(node.func)
        return ""

def parse_file_for_crypto(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding='utf-8', errors='ignore')
    tree = ast.parse(text)
    visitor = CryptoUsageVisitor()
    visitor.visit(tree)

    matches = []
    for imp in visitor.imports:
        mod = imp['module']
        name = imp['name']
        ln = imp['lineno']
        if mod.startswith("cryptography.hazmat.primitives.asymmetric"):
            if name == "rsa" or (name and "rsa" in name.lower()):
                matches.append({'type': 'RSA_IMPORT', 'line': ln, 'detail': f"{mod}.{name}"})
            if name == "ec" or (name and "ec" in name.lower()):
                matches.append({'type': 'ECC_IMPORT', 'line': ln, 'detail': f"{mod}.{name}"})
        if mod == "Crypto.PublicKey" or mod.startswith("Crypto.PublicKey"):
            if name == "RSA" or (name and "RSA" in name):
                matches.append({'type': 'PYCRYPTODOME_RSA', 'line': ln, 'detail': f"{mod}.{name}"})
        if mod == "paramiko" or mod.startswith("paramiko"):
            matches.append({'type': 'PARAMIKO_MODULE', 'line': ln, 'detail': mod})

    for c in visitor.calls:
        f = c['func']
        ln = c['lineno']
        if f.endswith("rsa.generate_private_key") or ("generate_private_key" in f and "rsa" in f):
            matches.append({'type': 'RSA_KEYGEN', 'line': ln, 'detail': f})
        if f.endswith("ec.generate_private_key") or ("generate_private_key" in f and "ec" in f):
            matches.append({'type': 'ECC_KEYGEN', 'line': ln, 'detail': f})
        if f.endswith("RSA.generate") or f == "RSA.generate":
            matches.append({'type': 'PYCRYPTODOME_RSA_GEN', 'line': ln, 'detail': f})
        if "paramiko.RSAKey" in f or f.endswith("RSAKey.from_private_key"):
            matches.append({'type': 'PARAMIKO_RSA', 'line': ln, 'detail': f})
        if "generateKeyPair" in f or "generate_keypair" in f:
            matches.append({'type': 'GENERIC_KEYGEN', 'line': ln, 'detail': f})

    return {'imports': visitor.imports, 'calls': visitor.calls, 'matches': matches}

def scan_directory_ast(path: str = "."):
    results = {}
    for p in Path(path).rglob("*.py"):
        if "quantum_armor" in str(p):
            continue
        try:
            r = parse_file_for_crypto(p)
            if r['matches']:
                results[str(p)] = r['matches']
        except Exception:
            continue
    return results