"""Comando clone - clona disco."""
from ..core.disk_manager import DiskManager
import shutil

def execute(args):
    shutil.copy(args.source, args.dest)
    print(f"✅ Disco clonado: {args.source} -> {args.dest}")
