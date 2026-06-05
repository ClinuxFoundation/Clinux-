"""Modelo de rootfs."""
from dataclasses import dataclass

@dataclass
class Rootfs:
    name: str
    path: str
    distro: str = "unknown"
    arch: str = "x86_64"
