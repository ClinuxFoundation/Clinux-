#!/bin/bash
# Instalar dependências do CLINUX

echo "Instalando dependências..."

# Debian/Ubuntu
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y qemu-system-x86 qemu-utils proot
fi

# Termux
if [ -d /data/data/com.termux ]; then
    pkg install -y qemu-system-x86-64-headless proot
fi

echo "✅ Dependências instaladas!"
