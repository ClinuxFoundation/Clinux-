"""Comando list."""
from ..core.storage_manager import StorageManager

def execute(args):
    s = StorageManager()
    vms = s.list_vms()
    roots = s.list_roots()
    if vms:
        print("📦 VMs:", ", ".join(vms))
    if roots:
        print("🌱 Rootfs:", ", ".join(roots))
