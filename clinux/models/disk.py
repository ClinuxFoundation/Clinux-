"""Modelo de disco."""
from dataclasses import dataclass

@dataclass
class Disk:
    path: str
    format: str = "qcow2"
    size: str = "20G"
    used: str = "0"
