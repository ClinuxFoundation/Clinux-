"""Testes do comando proot."""
import pytest
from clinux.commands.proot import execute as proot_execute

def test_proot_rootfs_not_found():
    class Args:
        rootfs = "/tmp/nao_existe.tar.gz"
    with pytest.raises(SystemExit):
        proot_execute(Args())
