"""Adaptador de salida: guarda las fotografías en una carpeta local."""
import os
import uuid

from app.domain.reporte import FotoAdjunta
from app.ports.foto_storage import FotoStorage


class FotoStorageLocal(FotoStorage):
    def __init__(self, carpeta):
        self._carpeta = carpeta

    def guardar(self, foto: FotoAdjunta) -> str:
        os.makedirs(self._carpeta, exist_ok=True)
        extension = os.path.splitext(foto.nombre_archivo)[1].lower()
        ruta = os.path.join(self._carpeta, f"{uuid.uuid4().hex}{extension}")
        with open(ruta, "wb") as archivo:
            archivo.write(foto.contenido)
        return ruta

    def eliminar(self, ruta: str) -> None:
        if os.path.exists(ruta):
            os.remove(ruta)
