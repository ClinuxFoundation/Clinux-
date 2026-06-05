"""Testes dos adapters."""
from clinux.adapters.system_adapter import SystemAdapter

def test_system_adapter():
    assert SystemAdapter.get_arch() is not None
    assert SystemAdapter.get_os() in ["Linux", "Darwin", "Windows"]
