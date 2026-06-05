"""Testes do SnapshotManager."""
from clinux.core.snapshot_manager import SnapshotManager

def test_snapshot_manager_init():
    snap = SnapshotManager()
    assert snap is not None
