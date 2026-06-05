"""Serviço de validação."""
from pathlib import Path

class ValidationService:
    @staticmethod
    def check_iso(path):
        return Path(path).exists() and Path(path).suffix == ".iso"
    
    @staticmethod
    def check_vm(name, storage):
        return storage.get_vm(name) is not None
    
    @staticmethod
    def check_deps():
        import subprocess
        deps = {"qemu-system-x86_64": False, "proot": False, "qemu-img": False}
        for dep in deps:
            try:
                subprocess.run([dep, "--version"], capture_output=True)
                deps[dep] = True
            except FileNotFoundError:
                pass
        return deps
