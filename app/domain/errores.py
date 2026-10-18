"""Errores del dominio. No dependen de ninguna tecnología externa."""


class ErrorDeDominio(Exception):
    pass


class ValidacionError(ErrorDeDominio):
    """Un dato del reporte no cumple una regla de negocio."""

    def __init__(self, campo, mensaje):
        super().__init__(mensaje)
        self.campo = campo
        self.mensaje = mensaje


class PersistenciaError(ErrorDeDominio):
    """No se pudo guardar o leer en el almacenamiento."""
