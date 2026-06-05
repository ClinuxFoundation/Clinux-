"""Modelo de configuração."""
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    home: str = str(Path.home() / ".clinux")
    qemu_bin: str = "qemu-system-x86_64"
    default_memory: str = "2G"
    default_cpu: str = "2"
    default_disk: str = "20G"
