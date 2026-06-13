"""Gerenciador PRoot - Suporte completo para Android e PC."""
import subprocess
import sys
import tarfile
import shutil
from pathlib import Path
from .base_manager import BaseManager
from .storage_manager import StorageManager
from clinux.adapters.proot_adapter import PRootAdapter


class PRootManager(BaseManager):
    def __init__(self):
        self.storage = StorageManager()
        self.adapter = PRootAdapter()
        self.is_termux = Path("/data/data/com.termux/files").exists()
        self.is_android = Path("/system/build.prop").exists()
    
    def check_dependencies(self):
        """Verifica dependências do PRoot."""
        if not shutil.which("proot"):
            print("❌ Instale proot:")
            if self.is_termux:
                print("   Termux: pkg install proot")
            else:
                print("   Linux: sudo apt install proot")
            sys.exit(1)
    
    def validate(self, target):
        """Valida se o alvo existe."""
        return Path(target).exists()
    
    def _extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs usando o adapter."""
        print(f"📦 Extraindo rootfs...")
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with tarfile.open(archive_path) as tar:
                for member in tar.getmembers():
                    if member.isdev():
                        continue
                    try:
                        tar.extract(member, dest_dir)
                    except Exception as e:
                        print(f"⚠️  Erro ao extrair {member.name}: {e}")
            
            # Cria diretórios essenciais
            for d in ["dev", "proc", "sys", "tmp", "home", "root"]:
                (dest_dir / d).mkdir(exist_ok=True)
            
            print("✅ Extração concluída!")
        except Exception as e:
            print(f"❌ Erro na extração: {e}")
            raise
    
    def _find_shell(self, target):
        """Encontra shell disponível no rootfs."""
        shells = ["/bin/bash", "/bin/zsh", "/bin/ash", "/bin/sh"]
        for sh in shells:
            if (Path(target) / sh.lstrip("/")).exists():
                return sh
        return "/bin/sh"
    
    def start(self, rootfs_path):
        """Inicia ambiente PRoot.
        
        Args:
            rootfs_path: Caminho para o rootfs (arquivo tar ou diretório)
        """
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            sys.exit(1)
        
        name = rootfs_path.stem.replace(".tar", "")
        
        # Extrai se for arquivo tar
        if str(rootfs_path).endswith((".tar.gz", ".tgz", ".tar")):
            dest = self.storage.roots / name
            if not dest.exists() or not any(dest.iterdir()):
                self._extract_rootfs(rootfs_path, dest)
            target = dest
        else:
            target = rootfs_path
        
        # Registra no storage
        if not self.storage.get_root(name):
            self.storage.add_root(name, target)
        
        shell = self._find_shell(target)
        
        # Inicia com o adapter
        print(f"🌱 Iniciando ambiente PRoot '{name}'...")
        print(f"   Shell: {shell}")
        print(f"   Plataforma: {'Termux/Android' if self.is_termux else 'Linux'}")
        print(f"   Digite 'exit' para sair\n")
        
        try:
            self.adapter.start(str(target), shell=shell)
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
        except Exception as e:
            print(f"❌ Erro: {e}")
            sys.exit(1)
    
    def run_command(self, rootfs_path, command):
        """Executa comando dentro do PRoot.
        
        Args:
            rootfs_path: Caminho para o rootfs
            command: Comando a executar (string ou lista)
        
        Returns:
            Código de retorno
        """
        self.check_dependencies()
        
        rootfs_path = Path(rootfs_path)
        if not rootfs_path.exists():
            print(f"❌ Rootfs não encontrado: {rootfs_path}")
            return 1
        
        try:
            result = self.adapter.run_command(str(rootfs_path), command)
            return result.returncode
        except Exception as e:
            print(f"❌ Erro ao executar comando: {e}")
            return 1
    
    def extract_rootfs(self, archive_path, dest_dir):
        """Extrai rootfs manualmente.
        
        Args:
            archive_path: Caminho do arquivo tar
            dest_dir: Diretório de destino
        
        Returns:
            Caminho do diretório extraído
        """
        return self.adapter.extract(archive_path, dest_dir)
