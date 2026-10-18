"""Raíz de composición: conecta el caso de uso con sus adaptadores."""
from types import SimpleNamespace

from flask import Flask

from app.adapters.entrada.reporte_controller import crear_blueprint
from app.adapters.salida.foto_storage_local import FotoStorageLocal
from app.adapters.salida.reporte_repository_sqlite import ReporteRepositorySQLite
from app.application.registrar_reporte import RegistrarReporte
from app.infrastructure.config import obtener_configuracion
from app.infrastructure.database import Database


def create_app(configuracion=None):
    config = configuracion or obtener_configuracion()
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

    database = Database(config["DATABASE_PATH"])
    database.inicializar()
    repositorio = ReporteRepositorySQLite(database)
    almacen = FotoStorageLocal(config["UPLOAD_DIR"])
    caso_uso = RegistrarReporte(repositorio, almacen)

    app.register_blueprint(crear_blueprint(caso_uso, repositorio))
    app.pmv1 = SimpleNamespace(db=database, repo=repositorio, fotos=almacen, config=config)
    return app
