"""Validadores de entrada."""
from pathlib import Path
from .constants import ISO_EXT, TAR_EXT

def validate_iso(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"ISO não encontrada: {path}")
    if p.suffix.lower() != ISO_EXT:
        raise ValueError(f"Arquivo não é ISO: {path}")
    return True

def validate_rootfs(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Rootfs não encontrado: {path}")
    return True