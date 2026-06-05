#!/usr/bin/env python3
"""Exemplo: Iniciar ambiente PRoot rapidamente."""
import sys
sys.path.insert(0, '..')

from clinux.core.proot_manager import PRootManager

def main():
    proot = PRootManager()
    rootfs = "alpine-minirootfs.tar.gz"
    
    print(f"Iniciando PRoot com: {rootfs}")
    proot.start(rootfs)

if __name__ == "__main__":
    main()
