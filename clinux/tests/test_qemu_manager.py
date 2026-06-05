"""Testes do QEMUManager."""
import pytest
from clinux.core.qemu_manager import QEMUManager

def test_qemu_manager_init():
    qemu = QEMUManager()
    assert qemu is not None

def test_check_dependencies():
    qemu = QEMUManager()
    try:
        qemu.check_dependencies()
    except SystemExit:
        pytest.skip("QEMU não instalado")
