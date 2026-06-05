"""Teste de ciclo de vida completo da VM."""
import pytest
from pathlib import Path

def test_vm_lifecycle(temp_dir):
    from clinux.core.storage_manager import StorageManager
    storage = StorageManager(base_dir=temp_dir)
    
    # Criar
    storage.add_vm("lifecycle-test")
    assert "lifecycle-test" in storage.list_vms()
    
    # Verificar
    vm = storage.get_vm("lifecycle-test")
    assert vm is not None
    
    # Deletar
    storage.delete("lifecycle-test")
    assert "lifecycle-test" not in storage.list_vms()
