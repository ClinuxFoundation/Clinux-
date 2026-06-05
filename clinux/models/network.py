"""Modelo de rede."""
from dataclasses import dataclass

@dataclass
class Network:
    mode: str = "user"
    mac: str = ""
    ports: list = None
    bridge: str = ""
