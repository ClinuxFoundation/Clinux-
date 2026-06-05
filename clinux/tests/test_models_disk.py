"""Testes do modelo Disk."""
from clinux.models.disk import Disk

def test_disk_creation():
    disk = Disk(path="/tmp/test.qcow2")
    assert disk.format == "qcow2"
    assert disk.size == "20G"
