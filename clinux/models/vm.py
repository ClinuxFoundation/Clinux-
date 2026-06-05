"""Modelo de VM."""
from dataclasses import dataclass

@dataclass
class VM:
    name: str
    disk: str
    memory: str = "2G"
    cpu: str = "2"
    arch: str = "x86_64"
    running: bool = False
