"""Puerto de salida: contrato que debe cumplir cualquier almacenamiento de reportes."""
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.reporte import Reporte


class ReporteRepository(ABC):
    @abstractmethod
    def guardar(self, reporte: Reporte) -> Reporte:
        """Guarda el reporte y devuelve la misma entidad con su identificador."""

    @abstractmethod
    def obtener(self, id_reporte: int) -> Optional[Reporte]:
        """Devuelve el reporte o None si no existe."""
