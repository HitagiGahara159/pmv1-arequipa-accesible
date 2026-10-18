"""Reglas de validación de un reporte (versión 0.1)."""
from dataclasses import dataclass

from app.domain.errores import ValidacionError
from app.domain.reporte import TIPOS_BARRERA


DESCRIPCION_MAX = 500

# Area referencial de Arequipa metropolitana (debe validarse con la municipalidad)
LATITUD_MIN, LATITUD_MAX = -16.55, -16.25
LONGITUD_MIN, LONGITUD_MAX = -71.75, -71.35


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

    descripcion = (s.descripcion or "").strip()
    if not descripcion:
        raise ValidacionError("descripcion", "La descripción es obligatoria.")
    if len(descripcion) > DESCRIPCION_MAX:
        raise ValidacionError("descripcion", f"La descripción no puede superar {DESCRIPCION_MAX} caracteres.")

    try:
        latitud = float(s.latitud)
        longitud = float(s.longitud)
    except (TypeError, ValueError):
        raise ValidacionError("ubicacion", "La ubicación indicada no es válida.")

    if not (LATITUD_MIN <= latitud <= LATITUD_MAX and LONGITUD_MIN <= longitud <= LONGITUD_MAX):
        raise ValidacionError("ubicacion", "La ubicación debe estar dentro del área de Arequipa.")

    if s.foto is None or not s.foto.contenido:
        raise ValidacionError("foto", "La fotografía es obligatoria.")

    return DatosValidados(id_tipo, descripcion, latitud, longitud)
