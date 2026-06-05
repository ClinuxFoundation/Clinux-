"""Configuração global dos testes."""
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

@pytest.fixture
def storage(temp_dir):
    from clinux.core.storage_manager import StorageManager
    return StorageManager(base_dir=temp_dir)
