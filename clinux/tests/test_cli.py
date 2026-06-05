"""Testes da CLI."""
import pytest
from clinux.cli import main

def test_main_no_args():
    with pytest.raises(SystemExit):
        main()

def test_help():
    import subprocess
    result = subprocess.run(["clinux", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
