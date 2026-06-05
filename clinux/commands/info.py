"""Comando info."""
from ..core.storage_manager import StorageManager
from ..core.disk_manager import DiskManager

def execute(args):
    s = StorageManager()
    vm = s.get_vm(args.name)
    if vm:
        print(DiskManager.info(vm["disk"]))
    else:
        print("VM não encontrada.")
