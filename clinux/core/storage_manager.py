"""Gerenciador de armazenamento."""
import json
import shutil
from pathlib import Path
from ..config import BASE_DIR
from ..constants import VM_DIR, DISKS_DIR, ROOTS_DIR, SNAPS_DIR

class StorageManager:
    def __init__(self, base_dir=None):
        if base_dir:
            self.base = Path(base_dir)
        else:
            self.base = BASE_DIR
        
        self.vms = self.base / VM_DIR
        self.disks = self.base / DISKS_DIR
        self.snaps = self.base / SNAPS_DIR
        self.roots = self.base / ROOTS_DIR
        
        for d in [self.vms, self.disks, self.snaps, self.roots]:
            d.mkdir(parents=True, exist_ok=True)
    
    # -------- VMs --------
    def add_vm(self, name):
        config = {"name": name, "disk": str(self.disks / f"{name}.qcow2"), "type": "vm"}
        with open(self.vms / f"{name}.json", "w") as f:
            json.dump(config, f, indent=2)
        return config
    
    def get_vm(self, name):
        p = self.vms / f"{name}.json"
        return json.load(open(p)) if p.exists() else None
    
    def list_vms(self):
        return sorted([f.stem for f in self.vms.glob("*.json")])
    
    def delete_vm(self, name):
        vm = self.get_vm(name)
        if vm:
            Path(vm["disk"]).unlink(missing_ok=True)
            (self.vms / f"{name}.json").unlink()
            return True
        return False
    
    # -------- Rootfs --------
    def add_root(self, name, source_path):
        dest = self.roots / name
        
        # Se for diretório, copia
        if Path(source_path).is_dir() and str(source_path) != str(dest):
            if not dest.exists():
                shutil.copytree(source_path, dest)
        elif Path(source_path).is_dir():
            pass  # Já está no lugar certo
        
        config = {
            "name": name,
            "path": str(dest if dest.exists() else source_path),
            "type": "rootfs"
        }
        with open(self.roots / f"{name}.json", "w") as f:
            json.dump(config, f, indent=2)
        return config
    
    def get_root(self, name):
        p = self.roots / f"{name}.json"
        return json.load(open(p)) if p.exists() else None
    
    def list_roots(self):
        return sorted([f.stem for f in self.roots.glob("*.json")])
    
    def delete_root(self, name):
        root = self.get_root(name)
        if root:
            root_path = Path(root["path"])
            if root_path.exists():
                shutil.rmtree(root_path)
            (self.roots / f"{name}.json").unlink()
            return True
        return False
    
    # -------- Genérico --------
    def delete(self, name):
        """Remove VM ou rootfs."""
        if self.get_vm(name):
            return self.delete_vm(name)
        elif self.get_root(name):
            return self.delete_root(name)
        return False
