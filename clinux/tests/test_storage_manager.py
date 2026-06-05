"""Testes do StorageManager."""
import json
from clinux.core.storage_manager import StorageManager

def test_add_vm(storage):
    storage.add_vm("test-vm")
    assert "test-vm" in storage.list_vms()

def test_get_vm(storage):
    storage.add_vm("test-vm")
    vm = storage.get_vm("test-vm")
    assert vm["name"] == "test-vm"
    assert "disk" in vm

def test_delete_vm(storage):
    storage.add_vm("test-vm")
    storage.delete("test-vm")
    assert "test-vm" not in storage.list_vms()

def test_list_vms_empty(storage):
    assert storage.list_vms() == []
