"""Entidades del dominio: Reporte, estados y catálogo de tipos de barrera."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EstadoReporte(str, Enum):
    PENDIENTE = "PENDIENTE"
    REVISADO = "REVISADO"
    DERIVADO = "DERIVADO"
    ATENDIDO = "ATENDIDO"


# Mismo catálogo de tipos que usa la PoC de IA (variable tipo_barrera)
TIPOS_BARRERA = {
    1: "Vereda dañada",
    2: "Sin rampa",
    3: "Rampa deteriorada",
    4: "Obstáculo en la vía pública",
    5: "Desnivel",
}


@dataclass
class FotoAdjunta:
    nombre_archivo: str
    contenido: bytes


@dataclass
class Reporte:
    id_tipo: int
    descripcion: str
    latitud: float
    longitud: float
    foto_ruta: str
    canal: str = "WEB"
    estado: EstadoReporte = EstadoReporte.PENDIENTE
    id_reporte: Optional[int] = None
    fecha_creacion: Optional[str] = None

    @property
    def codigo_caso(self):
        return f"AQP-{self.id_reporte:06d}" if self.id_reporte else None
