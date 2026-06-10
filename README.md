# CLINUX

![Open Source](https://img.shields.io/badge/open--source-yes-brightgreen)

Ferramenta CLI para gerenciar ambientes Linux usando QEMU e PRoot.

## Instalação

```bash
pip install -e .
```

Uso

```bash
clinux install ubuntu.iso
clinux run minha-vm
clinux proot ./rootfs.tar.gz
clinux list
clinux delete minha-vm
clinux snapshot save minha-vm
```

Requisitos

· Python 3.6+
· QEMU (para VMs)
· PRoot (para ambientes rootfs)

## License
This project is open-source under the GPL-v3.0 License.

© Davi - Clinux Project
