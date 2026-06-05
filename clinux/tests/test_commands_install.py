"""Testes do comando install."""
import pytest

def test_install_requires_iso():
    from clinux.commands import install
    class Args:
        iso = "nao_existe.iso"
    with pytest.raises(FileNotFoundError):
        install.execute(Args())
