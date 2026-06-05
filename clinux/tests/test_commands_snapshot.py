"""Testes do comando snapshot."""
from clinux.commands.snapshot import execute

def test_snapshot_save_invalid():
    class Args:
        action = "save"
        name = "vm_invalida"
    try:
        execute(Args())
    except:
        pass
