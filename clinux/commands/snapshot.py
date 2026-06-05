"""Comando snapshot."""
from ..core.snapshot_manager import SnapshotManager

def execute(args):
    snap = SnapshotManager()
    if args.action == "save":
        snap.save(args.name)
    else:
        snap.load(args.name)
