"""Comando config."""
import json
from ..core.storage_manager import StorageManager

def execute(args):
    s = StorageManager()
    vm = s.get_vm(args.name)
    if vm:
        print(json.dumps(vm, indent=2))
    else:
        print("VM não encontrada.")
