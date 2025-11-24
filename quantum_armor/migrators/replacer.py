import ast
from .crypto_shims import KyberShim, DilithiumShim

class PQCMigrator(ast.NodeTransformer):
    def __init__(self, algo: str = "kyber"):
        self.changes_made = False
        self.algo = algo.lower()
        self.kyber = KyberShim()                     
        self.dilithium = None                        
        if self.algo == "dilithium":
            self.dilithium = DilithiumShim()
        self.pqc_import_added = False

    def visit_Call(self, node):
        if (isinstance(node.func, ast.Attribute) and
            node.func.attr == "generate_private_key" and
            hasattr(node.func.value, "id") and
            node.func.value.id == "rsa"):
            self.changes_made = True
            return ast.Call(
                func=ast.Attribute(value=ast.Name("KyberShim"), attr="keygen"),
                args=[], keywords=[]
            )
        return self.generic_visit(node)