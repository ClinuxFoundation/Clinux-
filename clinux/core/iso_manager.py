"""Gerenciador de ISOs."""
from pathlib import Path
import subprocess

class ISOManager:
    @staticmethod
    def verify(path):
        return Path(path).suffix.lower() == ".iso" and Path(path).exists()
    
    @staticmethod
    def info(path):
        result = subprocess.run(["file", str(path)], capture_output=True, text=True)
        return result.stdout
    
    @staticmethod
    def mount(path, mount_point):
        Path(mount_point).mkdir(exist_ok=True)
        subprocess.run(["sudo", "mount", "-o", "loop", str(path), str(mount_point)])
    
    @staticmethod
    def unmount(mount_point):
        subprocess.run(["sudo", "umount", str(mount_point)])
