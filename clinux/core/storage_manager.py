"""Gerenciador de armazenamento."""
import json
import shutil
from pathlib import Path
from ..config import BASE_DIR
from ..constants import VM_DIR, DISKS_DIR, ROOTS_DIR

class StorageManager:
    def __init__(self):
        self.base = BASE_DIR
        self.vms = self.base / VM_DIR
        self.disks = self.base / DISKS_DIR
        self.roots = self.base / ROOTS_DIR
        for d in [self.vms, self.disks, self.roots]:
            d.mkdir(parents=True, exist_ok=True)
    
    def add_vm(self, name):
        config = {"name": name, "disk": str(self.disks / f"{name}.qcow2")}
        with open(self.vms / f"{name}.json", "w") as f:
            json.dump(config, f)
        return config
    
    def get_vm(self, name):
        p = self.vms / f"{name}.json"
        return json.load(open(p)) if p.exists() else None
    
    def list_vms(self):
        return [f.stem for f in self.vms.glob("*.json")]
    
    def list_roots(self):
        return [f.stem for f in self.roots.glob("*.json")]
    
    def delete(self, name):
        vm = self.get_vm(name)
        if vm:
            Path(vm["disk"]).unlink(missing_ok=True)
            (self.vms / f"{name}.json").unlink()
            return
        root = self.roots / name
        if root.exists():
            shutil.rmtree(root)
            (self.roots / f"{name}.json").unlink(missing_ok=True)