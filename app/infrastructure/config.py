"""Configuración leída desde variables de entorno (sin secretos en el código)."""
import os
from pathlib import Path


def cargar_env(ruta=".env"):
    """Carga pares CLAVE=VALOR de un archivo .env si existe (sin dependencias externas)."""
    archivo = Path(ruta)
    if not archivo.exists():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip())


def obtener_configuracion():
    return {
        "DATABASE_PATH": os.getenv("DATABASE_PATH", "pmv1.db"),
        "UPLOAD_DIR": os.getenv("UPLOAD_DIR", "uploads"),
    }
