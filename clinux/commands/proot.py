"""Comando proot."""
from ..core.proot_manager import PRootManager

def execute(args):
    proot = PRootManager()
    proot.start(args.rootfs)
