"""Reglas de validación de un reporte (versión 0.1)."""
from dataclasses import dataclass

from app.domain.errores import ValidacionError
from app.domain.reporte import TIPOS_BARRERA


@dataclass
class SolicitudRegistro:
    """Datos crudos que llegan desde cualquier canal (web, WhatsApp...)."""
    id_tipo: object
    descripcion: object
    latitud: object
    longitud: object
    foto: object  # FotoAdjunta o None
    canal: str = "WEB"


@dataclass
class DatosValidados:
    id_tipo: int
    descripcion: str
    latitud: float
    longitud: float


def validar_solicitud(s):
    try:
        id_tipo = int(s.id_tipo)
    except (TypeError, ValueError):
        raise ValidacionError("id_tipo", "Seleccione un tipo de barrera válido.")
    if id_tipo not in TIPOS_BARRERA:
        raise ValidacionError("id_tipo", "Seleccione un tipo de barrera válido.")

    if not s.descripcion:
        raise ValidacionError("descripcion", "La descripción es obligatoria.")

    try:
        latitud = float(s.latitud)
        longitud = float(s.longitud)
    except (TypeError, ValueError):
        raise ValidacionError("ubicacion", "La ubicación indicada no es válida.")

    if s.foto is None or not s.foto.contenido:
        raise ValidacionError("foto", "La fotografía es obligatoria.")

    return DatosValidados(id_tipo, s.descripcion, latitud, longitud)
