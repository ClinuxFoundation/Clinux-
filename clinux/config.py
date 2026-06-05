"""Configurações globais do CLINUX."""
import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("CLINUX_HOME", Path.home() / ".clinux"))
QEMU_MEMORY = os.environ.get("QEMU_MEMORY", "2G")
QEMU_CPU = os.environ.get("QEMU_CPU", "2")
DISK_SIZE = os.environ.get("CLINUX_DISK_SIZE", "20G")