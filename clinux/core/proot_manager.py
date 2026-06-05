"""Gerenciador PRoot."""
import subprocess
import sys
import tarfile
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager

class PRootManager(BaseManager):
    def __init__(self):
        self.storage = StorageManager()
    
    def check_dependencies(self):
        try:
            subprocess.run(["proot", "--version"], capture_output=True)
        except FileNotFoundError:
            sys.exit("PRoot não instalado!")
    
    def validate(self, target):
        return Path(target).exists()
    
    def start(self, rootfs):
        self.check_dependencies()
        path = Path(rootfs)
        name = path.stem
        
        if str(path).endswith(".tar.gz"):
            dest = self.storage.roots / name
            if not dest.exists():
                dest.mkdir(parents=True)
                with tarfile.open(path) as t:
                    t.extractall(dest)
            target = dest
        else:
            target = path
        
        shell = "/bin/bash" if (Path(target)/"bin/bash").exists() else "/bin/sh"
        subprocess.run(["proot", "-r", str(target), "-w", "/", shell])