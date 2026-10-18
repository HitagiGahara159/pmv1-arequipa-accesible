"""Caso de uso HU-01: registrar un reporte de barrera de accesibilidad (versión 0.1)."""
from app.domain.reporte import Reporte
from app.domain.validaciones import SolicitudRegistro, validar_solicitud
from app.ports.foto_storage import FotoStorage
from app.ports.reporte_repository import ReporteRepository


class RegistrarReporte:
    def __init__(self, repositorio: ReporteRepository, almacen_fotos: FotoStorage):
        self._repo = repositorio
        self._fotos = almacen_fotos

    def ejecutar(self, solicitud: SolicitudRegistro) -> Reporte:
        datos = validar_solicitud(solicitud)
        ruta_foto = self._fotos.guardar(solicitud.foto)
        reporte = Reporte(
            id_tipo=datos.id_tipo,
            descripcion=datos.descripcion,
            latitud=datos.latitud,
            longitud=datos.longitud,
            foto_ruta=ruta_foto,
            canal=solicitud.canal,
        )
        return self._repo.guardar(reporte)
