"""Testes do PRootManager."""
import pytest
from clinux.core.proot_manager import PRootManager

def test_proot_manager_init():
    proot = PRootManager()
    assert proot is not None

def test_validate():
    proot = PRootManager()
    assert proot.validate("/tmp") == True
    assert proot.validate("/nao/existe") == False
