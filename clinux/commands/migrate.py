"""Comando migrate - converte formato de disco."""
from ..core.disk_manager import DiskManager

def execute(args):
    DiskManager.convert(args.path, args.format)
    print(f"✅ Disco convertido para {args.format}")
