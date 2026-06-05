"""Utilitários diversos."""
import subprocess
from pathlib import Path

def check_command(cmd):
    """Verifica se comando existe no sistema."""
    return subprocess.run(
        ["which", cmd], capture_output=True
    ).returncode == 0

def safe_path(path):
    """Converte para Path absoluto."""
    return Path(path).expanduser().resolve()

def human_size(bytes):
    """Converte bytes para formato legível."""
    for unit in ['B','KB','MB','GB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"