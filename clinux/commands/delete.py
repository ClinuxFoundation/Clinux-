"""Comando delete."""
from ..core.storage_manager import StorageManager

def execute(args):
    s = StorageManager()
    s.delete(args.name)
    print(f"✅ '{args.name}' removido.")
