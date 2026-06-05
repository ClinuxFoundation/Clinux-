"""Testes do comando run."""
from clinux.commands import run

def test_run_vm_not_found(storage):
    class Args:
        name = "vm_inexistente"
    from clinux.core.qemu_manager import QEMUManager
    qemu = QEMUManager()
    qemu.storage = storage
    try:
        qemu.run(Args.name)
    except SystemExit:
        pass
