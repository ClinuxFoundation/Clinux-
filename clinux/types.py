"""Tipos e dataclasses do sistema."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class VMConfig:
    name: str
    disk: str
    memory: str = "2G"
    cpu: str = "2"
    arch: str = "x86_64"

@dataclass
class RootfsConfig:
    name: str
    path: str
    distro: Optional[str] = None