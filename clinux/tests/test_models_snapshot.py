"""Testes do modelo Snapshot."""
from clinux.models.snapshot import Snapshot

def test_snapshot_creation():
    snap = Snapshot(name="snap1", vm_name="vm1")
    assert snap.name == "snap1"
    assert snap.vm_name == "vm1"
