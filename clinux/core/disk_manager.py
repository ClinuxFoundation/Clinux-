"""Gerenciador de discos virtuais."""
import subprocess
from pathlib import Path
from ..config import DISK_SIZE

class DiskManager:
    @staticmethod
    def create(path, size=DISK_SIZE, fmt="qcow2"):
        subprocess.run(["qemu-img", "create", "-f", fmt, str(path), size])
    
    @staticmethod
    def info(path):
        result = subprocess.run(
            ["qemu-img", "info", str(path)], capture_output=True, text=True
        )
        return result.stdout
    
    @staticmethod
    def resize(path, size):
        subprocess.run(["qemu-img", "resize", str(path), size])
    
    @staticmethod
    def convert(path, dest_fmt):
        dest = str(path).replace(".qcow2", f".{dest_fmt}")
        subprocess.run(["qemu-img", "convert", "-f", "qcow2", "-O", dest_fmt, str(path), dest])
