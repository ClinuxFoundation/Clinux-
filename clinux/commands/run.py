"""Comando run."""
from ..core.qemu_manager import QEMUManager

def execute(args):
    qemu = QEMUManager()
    qemu.run(args.name)
