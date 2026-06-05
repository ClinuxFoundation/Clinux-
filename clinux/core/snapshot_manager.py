"""Gerenciador de snapshots."""
import subprocess
from .storage_manager import StorageManager

class SnapshotManager:
    def __init__(self):
        self.storage = StorageManager()
    
    def save(self, vm_name):
        vm = self.storage.get_vm(vm_name)
        subprocess.run(["qemu-img", "snapshot", "-c", "saved", vm["disk"]])
    
    def load(self, vm_name):
        vm = self.storage.get_vm(vm_name)
        subprocess.run(["qemu-img", "snapshot", "-a", "saved", vm["disk"]])
    
    def list_snapshots(self, vm_name):
        vm = self.storage.get_vm(vm_name)
        result = subprocess.run(
            ["qemu-img", "snapshot", "-l", vm["disk"]], capture_output=True, text=True
        )
        return result.stdout