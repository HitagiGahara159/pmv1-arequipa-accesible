"""Acceso a la base de datos SQLite: conexión e inicialización del esquema."""
import sqlite3
from pathlib import Path

from app.domain.reporte import TIPOS_BARRERA

RUTA_SCHEMA = Path(__file__).resolve().parents[2] / "db" / "schema.sql"


class Database:
    def __init__(self, path):
        self.path = path

    def conectar(self):
        conexion = sqlite3.connect(self.path)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def inicializar(self):
        """Crea las tablas y carga el catálogo de tipos de barrera."""
        conexion = self.conectar()
        try:
            conexion.executescript(RUTA_SCHEMA.read_text(encoding="utf-8"))
            conexion.executemany(
                "INSERT OR IGNORE INTO tipo_barrera (id_tipo, nombre) VALUES (?, ?)",
                list(TIPOS_BARRERA.items()),
            )
            conexion.commit()
        finally:
            conexion.close()
