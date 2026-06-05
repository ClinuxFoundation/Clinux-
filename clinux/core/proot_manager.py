"""Gerenciador PRoot - Força QEMU no Termux para resolver linker."""
import subprocess
import sys
import tarfile
import shutil
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager


class PRootManager(BaseManager):
    def __init__(self):
        self.storage = StorageManager()
        self.is_termux = Path("/data/data/com.termux/files").exists()
    
    def check_dependencies(self):
        if not shutil.which("proot"):
            print("❌ Instale proot:")
            print("   Termux: pkg install proot")
            print("   Linux: sudo apt install proot")
            sys.exit(1)
        
        if self.is_termux and not shutil.which("qemu-aarch64"):
            print("❌ Instale QEMU user mode:")
            print("   pkg install qemu-user-aarch64")
            sys.exit(1)
    
    def validate(self, target):
        return Path(target).exists()
    
    def _extract_rootfs(self, archive_path, dest_dir):
        print(f"📦 Extraindo rootfs...")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(archive_path) as tar:
            for member in tar.getmembers():
                if member.isdev():
                    continue
                try:
                    tar.extract(member, dest_dir)
                except:
                    pass
        
        for d in ["dev", "proc", "sys", "tmp"]:
            (dest_dir / d).mkdir(exist_ok=True)
        
        print("✅ Extração concluída!")
    
    def _find_shell(self, target):
        for sh in ["/bin/bash", "/bin/zsh", "/bin/ash", "/bin/sh"]:
            if (Path(target) / sh.lstrip("/")).exists():
                return sh
        return "/bin/sh"
    
    def start(self, rootfs_path):
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        name = rootfs_path.stem.replace(".tar", "")
        
        if str(rootfs_path).endswith((".tar.gz", ".tgz", ".tar")):
            dest = self.storage.roots / name
            if not dest.exists() or not any(dest.iterdir()):
                self._extract_rootfs(rootfs_path, dest)
            target = dest
        else:
            target = rootfs_path
        
        if not self.storage.get_root(name):
            self.storage.add_root(name, target)
        
        shell = self._find_shell(target)
        
        cmd = ["proot", "-r", str(target)]
        
        if self.is_termux:
            cmd.extend(["-q", "qemu-aarch64"])
            print("🔄 Usando QEMU para compatibilidade...")
        
        cmd.extend([
            "-b", "/dev:/dev",
            "-b", "/proc:/proc",
            "-b", "/sys:/sys",
            "-w", "/",
            shell
        ])
        
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Digite 'exit' para sair\n")
        
        subprocess.run(cmd, check=False)
