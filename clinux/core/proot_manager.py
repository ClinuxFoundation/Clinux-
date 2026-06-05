"""Gerenciador PRoot."""
import subprocess
import sys
import tarfile
import os
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager

class PRootManager(BaseManager):
    """Gerencia ambientes Linux leves usando PRoot."""
    
    def __init__(self):
        self.storage = StorageManager()
    
    def check_dependencies(self):
        """Verifica se PRoot está instalado."""
        try:
            subprocess.run(
                ["proot", "--version"],
                capture_output=True,
                check=False
            )
        except FileNotFoundError:
            print("❌ ERRO: PRoot não está instalado!")
            print("   Termux: pkg install proot")
            print("   Linux: sudo apt install proot")
            sys.exit(1)
    
    def validate(self, target):
        """Valida se o rootfs existe."""
        return Path(target).exists()
    
    def _extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs ignorando dispositivos (seguro para Termux)."""
        print(f"📦 Extraindo rootfs para {dest_dir}...")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(archive_path) as tar:
            for member in tar.getmembers():
                # Pula arquivos de dispositivo (major/minor)
                if member.isdev():
                    print(f"  ⏭️  Pulando dispositivo: {member.name}")
                    continue
                # Pula hard links quebrados
                if member.islnk():
                    try:
                        tar.extract(member, dest_dir)
                    except:
                        print(f"  ⏭️  Pulando link: {member.name}")
                    continue
                try:
                    tar.extract(member, dest_dir)
                except PermissionError:
                    print(f"  ⚠️  Permissão negada: {member.name}")
                except OSError as e:
                    print(f"  ⚠️  Erro ao extrair {member.name}: {e}")
        
        # Cria diretórios essenciais se não existirem
        for d in ["dev", "proc", "sys", "tmp"]:
            (dest_dir / d).mkdir(exist_ok=True)
        
        print("✅ Extração concluída!")
    
    def start(self, rootfs_path):
        """Inicia ambiente PRoot."""
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        # Gera nome baseado no caminho
        name = rootfs_path.stem.replace(".tar", "")
        
        # Se for tarball, extrai primeiro
        if str(rootfs_path).endswith((".tar.gz", ".tgz", ".tar")):
            dest = self.storage.roots / name
            if not dest.exists() or not any(dest.iterdir()):
                self._extract_rootfs(rootfs_path, dest)
            target = dest
        else:
            target = rootfs_path
        
        # Registra rootfs
        if not self.storage.get_root(name):
            self.storage.add_root(name, target)
        
        # Detecta shell disponível
        shell = "/bin/sh"
        for sh in ["/bin/bash", "/bin/zsh", "/bin/sh"]:
            if (Path(target) / sh.lstrip("/")).exists():
                shell = sh
                break
        
        # Monta binds essenciais
        binds = []
        for d in ["/dev", "/proc", "/sys"]:
            if Path(d).exists():
                binds.extend(["-b", f"{d}:{d}"])
        
        # Inicia PRoot
        cmd = ["proot"] + binds + ["-r", str(target), "-w", "/", shell]
        
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Digite 'exit' para sair\n")
        
        subprocess.run(cmd, check=False)
