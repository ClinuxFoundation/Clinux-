"""Teste de ciclo de vida do PRoot."""
import pytest

def test_proot_rootfs_registration(temp_dir):
    from clinux.core.storage_manager import StorageManager
    import json
    
    storage = StorageManager(base_dir=temp_dir)
    
    # Criar rootfs fake
    root_dir = temp_dir / "rootfs" / "test-root"
    root_dir.mkdir(parents=True)
    (root_dir / "bin").mkdir()
    (root_dir / "bin" / "bash").touch()
    
    config = {"name": "test-root", "path": str(root_dir), "type": "rootfs"}
    with open(storage.roots / "test-root.json", "w") as f:
        json.dump(config, f)
    
    assert "test-root" in storage.list_roots()
