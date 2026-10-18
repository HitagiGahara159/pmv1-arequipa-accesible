"""Adaptador de salida: implementa ReporteRepository sobre SQLite (versión 0.2)."""
import sqlite3
from typing import Optional

from app.domain.errores import PersistenciaError

from app.domain.reporte import EstadoReporte, Reporte
from app.infrastructure.database import Database
from app.ports.reporte_repository import ReporteRepository


class ReporteRepositorySQLite(ReporteRepository):
    def __init__(self, database: Database):
        self._db = database

    def guardar(self, reporte: Reporte) -> Reporte:
        conexion = None
        try:
            conexion = self._db.conectar()
            cursor = conexion.execute(
                "INSERT INTO reporte (id_tipo, canal, descripcion, latitud, longitud, foto_ruta, estado) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (reporte.id_tipo, reporte.canal, reporte.descripcion, reporte.latitud,
                 reporte.longitud, reporte.foto_ruta, reporte.estado.value),
            )
            reporte.id_reporte = cursor.lastrowid
            conexion.execute(
                "INSERT INTO historial_estado (id_reporte, estado) VALUES (?, ?)",
                (reporte.id_reporte, reporte.estado.value),
            )
            conexion.commit()
        except sqlite3.Error as error:
            raise PersistenciaError("No se pudo guardar el reporte.") from error
        finally:
            if conexion is not None:
                conexion.close()
        return reporte

    def obtener(self, id_reporte: int) -> Optional[Reporte]:
        conexion = None
        try:
            conexion = self._db.conectar()
            fila = conexion.execute("SELECT * FROM reporte WHERE id_reporte = ?", (id_reporte,)).fetchone()
        except sqlite3.Error as error:
            raise PersistenciaError("No se pudo leer el reporte.") from error
        finally:
            if conexion is not None:
                conexion.close()
        if fila is None:
            return None
        return Reporte(
            id_reporte=fila["id_reporte"], id_tipo=fila["id_tipo"], canal=fila["canal"],
            descripcion=fila["descripcion"], latitud=fila["latitud"], longitud=fila["longitud"],
            foto_ruta=fila["foto_ruta"], estado=EstadoReporte(fila["estado"]),
            fecha_creacion=fila["fecha_creacion"],
        )
