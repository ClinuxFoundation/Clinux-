"""Testes do modelo VM."""
from clinux.models.vm import VM

def test_vm_creation():
    vm = VM(name="test", disk="/tmp/test.qcow2")
    assert vm.name == "test"
    assert vm.memory == "2G"

def test_vm_defaults():
    vm = VM(name="default", disk="/tmp/disk.qcow2")
    assert vm.cpu == "2"
    assert vm.arch == "x86_64"
    assert vm.running == False
