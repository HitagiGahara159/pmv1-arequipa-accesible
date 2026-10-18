"""Puerto de salida: contrato para guardar las fotografías de los reportes."""
from abc import ABC, abstractmethod

from app.domain.reporte import FotoAdjunta


class FotoStorage(ABC):
    @abstractmethod
    def guardar(self, foto: FotoAdjunta) -> str:
        """Guarda la foto y devuelve su ruta/identificador."""

    @abstractmethod
    def eliminar(self, ruta: str) -> None:
        """Elimina una foto previamente guardada (si existe)."""
