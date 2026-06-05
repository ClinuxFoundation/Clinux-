"""Comando install."""
from ..core.qemu_manager import QEMUManager

def execute(args):
    qemu = QEMUManager()
    qemu.install(args.iso)
