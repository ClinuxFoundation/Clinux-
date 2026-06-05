"""Comando create - cria disco vazio."""
from ..core.disk_manager import DiskManager

def execute(args):
    DiskManager.create(args.path, args.size)
    print(f"✅ Disco criado: {args.path}")
