"""Gerenciador QEMU."""
import subprocess
import sys
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager

class QEMUManager(BaseManager):
    def __init__(self):
        self.storage = StorageManager()
    
    def check_dependencies(self):
        try:
            subprocess.run(["qemu-system-x86_64", "--version"], capture_output=True)
        except FileNotFoundError:
            sys.exit("QEMU não instalado!")
    
    def validate(self, target):
        return Path(target).exists()
    
    def install(self, iso):
        self.check_dependencies()
        name = Path(iso).stem
        config = self.storage.add_vm(name)
        subprocess.run(["qemu-img", "create", "-f", "qcow2", config["disk"], "20G"])
        subprocess.run([
            "qemu-system-x86_64", "-m", "2G", "-smp", "2",
            "-cdrom", iso, "-drive", f"file={config['disk']},format=qcow2",
            "-boot", "d", "-net", "user", "-net", "nic"
        ])
    
    def run(self, name):
        self.check_dependencies()
        vm = self.storage.get_vm(name) or sys.exit("VM não encontrada")
        subprocess.run([
            "qemu-system-x86_64", "-m", "2G",
            "-drive", f"file={vm['disk']},format=qcow2",
            "-net", "user", "-net", "nic"
        ])
    
    def snapshot_save(self, name):
        vm = self.storage.get_vm(name) or sys.exit("VM não encontrada")
        subprocess.run(["qemu-img", "snapshot", "-c", "main", vm["disk"]])
    
    def snapshot_load(self, name):
        vm = self.storage.get_vm(name) or sys.exit("VM não encontrada")
        subprocess.run(["qemu-img", "snapshot", "-a", "main", vm["disk"]])