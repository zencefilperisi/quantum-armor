# Shim / adapter: kyber-py ve dilithium-py'yi güvenli şekilde import eder
import importlib

class MissingPQCLibrary(Exception):
    pass

class KyberShim:
    def __init__(self):
        try:
            self.mod = importlib.import_module("kyber_py")
        except Exception as e:
            raise MissingPQCLibrary("kyber-py is required but not installed or failed to import") from e

    def keygen(self):
        if hasattr(self.mod, "ML_KEM_512"):
            return self.mod.ML_KEM_512.keygen()
        if hasattr(self.mod, "keygen"):
            return self.mod.keygen()
        raise MissingPQCLibrary("kyber_py does not expose a recognized keygen API")

    def encapsulate(self, pk):
        if hasattr(self.mod, "ML_KEM_512"):
            return self.mod.ML_KEM_512.encapsulate(pk)
        if hasattr(self.mod, "encapsulate"):
            return self.mod.encapsulate(pk)
        raise MissingPQCLibrary("kyber_py does not expose encapsulate")

    def decapsulate(self, sk, ct):
        if hasattr(self.mod, "ML_KEM_512"):
            return self.mod.ML_KEM_512.decapsulate(sk, ct)
        if hasattr(self.mod, "decapsulate"):
            return self.mod.decapsulate(sk, ct)
        raise MissingPQCLibrary("kyber_py does not expose decapsulate")

class DilithiumShim:
    def __init__(self):
        try:
            self.mod = importlib.import_module("dilithium_py")
        except Exception as e:
            raise MissingPQCLibrary("dilithium-py is required but not installed or failed to import") from e

    def keygen(self):
        if hasattr(self.mod, "Dilithium2"):
            return self.mod.Dilithium2.keygen()
        if hasattr(self.mod, "keygen"):
            return self.mod.keygen()
        raise MissingPQCLibrary("dilithium_py does not expose a recognized keygen API")

    def sign(self, sk, message: bytes):
        if hasattr(self.mod, "Dilithium2"):
            return self.mod.Dilithium2.sign(sk, message)
        if hasattr(self.mod, "sign"):
            return self.mod.sign(sk, message)
        raise MissingPQCLibrary("dilithium_py does not expose sign")

    def verify(self, pk, message: bytes, sig: bytes):
        if hasattr(self.mod, "Dilithium2"):
            return self.mod.Dilithium2.verify(pk, message, sig)
        if hasattr(self.mod, "verify"):
            return self.mod.verify(pk, message, sig)
        raise MissingPQCLibrary("dilithium_py does not expose verify")