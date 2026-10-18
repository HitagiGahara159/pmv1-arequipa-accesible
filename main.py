"""Punto de entrada del PMV1. Uso: python main.py"""
from app import create_app
from app.infrastructure.config import cargar_env

cargar_env()
app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
