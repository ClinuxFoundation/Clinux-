"""Exceções personalizadas do CLINUX."""

class CLINUXError(Exception):
    """Erro base do CLINUX."""
    pass

class VMNotFoundError(CLINUXError):
    """VM não encontrada."""
    pass

class DiskNotFoundError(CLINUXError):
    """Disco não encontrado."""
    pass

class DependencyError(CLINUXError):
    """Dependência não instalada."""
    pass

class RootfsError(CLINUXError):
    """Erro com rootfs."""
    pass