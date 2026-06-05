"""Serviço de verificação de saúde do sistema."""
import subprocess
import shutil
from pathlib import Path
from ..config import BASE_DIR

class HealthService:
    @staticmethod
    def check_disk_space():
        stat = shutil.disk_usage(BASE_DIR)
        return stat.free
    
    @staticmethod
    def check_qemu():
        return subprocess.run(["qemu-system-x86_64", "--version"], capture_output=True).returncode == 0
    
    @staticmethod
    def check_proot():
        return subprocess.run(["proot", "--version"], capture_output=True).returncode == 0
    
    @staticmethod
    def full_check():
        return {
            "qemu": HealthService.check_qemu(),
            "proot": HealthService.check_proot(),
            "disk_free": HealthService.check_disk_space()
        }
