"""Adaptador PRoot."""
import subprocess
import tarfile
from pathlib import Path

class PRootAdapter:
    def start(self, rootfs):
        return subprocess.run(["proot", "-r", str(rootfs), "-w", "/", "/bin/bash"])
    
    def extract(self, tarball, dest):
        Path(dest).mkdir(parents=True, exist_ok=True)
        with tarfile.open(tarball) as t:
            t.extractall(dest)
        return dest
