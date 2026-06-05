"""Gerenciador de rootfs."""
import tarfile
import shutil
from pathlib import Path
from ..constants import TAR_EXT

class RootfsManager:
    @staticmethod
    def extract(archive, dest):
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive) as t:
            t.extractall(dest)
    
    @staticmethod
    def validate(path):
        p = Path(path)
        return p.is_dir() or str(p).endswith(TAR_EXT)
    
    @staticmethod
    def get_shell(path):
        for sh in ["/bin/bash", "/bin/sh", "/bin/zsh"]:
            if (Path(path) / sh.lstrip("/")).exists():
                return sh
        return "/bin/sh"
