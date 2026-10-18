"""Pruebas del PMV1 - HU-01 Registrar reporte de barrera.

Cada prueba CP corresponde a un criterio de aceptación (CA) Given-When-Then.
"""
import base64
import io
import logging
import os
import shutil
import sqlite3
import tempfile
import unittest

from app import create_app

# PNG válido de 1x1 píxel
PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


class PruebasRegistroReporte(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)  # evita ruido de trazas en la salida de pruebas
        self.carpeta = tempfile.mkdtemp()
        self.ruta_bd = os.path.join(self.carpeta, "pmv1_test.db")
        self.ruta_fotos = os.path.join(self.carpeta, "uploads")
        self.app = create_app({"DATABASE_PATH": self.ruta_bd, "UPLOAD_DIR": self.ruta_fotos})
        self.cliente = self.app.test_client()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        shutil.rmtree(self.carpeta, ignore_errors=True)

    # ---------- utilidades ----------
    def datos_validos(self, **cambios):
        datos = {
            "id_tipo": "2",
            "descripcion": "No hay rampa frente al hospital",
            "latitud": "-16.3989",
            "longitud": "-71.5350",
            "foto": (io.BytesIO(PNG_1X1), "foto.png"),
        }
        datos.update(cambios)
        return datos

    def enviar(self, **cambios):
        return self.cliente.post("/api/reportes", data=self.datos_validos(**cambios),
                                 content_type="multipart/form-data")

    def contar(self, tabla):
        conexion = sqlite3.connect(self.ruta_bd)
        try:
            return conexion.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        finally:
            conexion.close()

    def fotos_guardadas(self):
        return os.listdir(self.ruta_fotos) if os.path.isdir(self.ruta_fotos) else []

    # ---------- CA-01: Registro exitoso ----------
    def test_cp01_registro_exitoso(self):
        """CP-01 (CA-01): registro exitoso con estado PENDIENTE e identificador"""
        resp = self.enviar()
        self.assertEqual(resp.status_code, 201)
        cuerpo = resp.get_json()
        self.assertEqual(cuerpo["estado"], "PENDIENTE")
        self.assertTrue(cuerpo["codigo_caso"].startswith("AQP-"))
        self.assertEqual(self.contar("reporte"), 1)
        self.assertEqual(self.contar("historial_estado"), 1)
        self.assertEqual(len(self.fotos_guardadas()), 1)

    def test_cp02_reporte_consultable(self):
        """CP-02 (CA-01): el reporte guardado se puede recuperar con sus datos"""
        id_reporte = self.enviar().get_json()["id"]
        resp = self.cliente.get(f"/api/reportes/{id_reporte}")
        self.assertEqual(resp.status_code, 200)
        cuerpo = resp.get_json()
        self.assertEqual(cuerpo["tipo_barrera"], "Sin rampa")
        self.assertEqual(cuerpo["descripcion"], "No hay rampa frente al hospital")
        self.assertEqual(cuerpo["estado"], "PENDIENTE")
        self.assertEqual(cuerpo["canal"], "WEB")

    # ---------- CA-02: Descripción obligatoria ----------
    def test_cp03_descripcion_vacia_rechazada(self):
        """CP-03 (CA-02): descripción vacía es rechazada con mensaje"""
        resp = self.enviar(descripcion="")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "La descripción es obligatoria.")
        self.assertEqual(self.contar("reporte"), 0)

    def test_cp04_descripcion_solo_espacios_rechazada(self):
        """CP-04 (CA-02): descripción con solo espacios es rechazada con mensaje"""
        resp = self.enviar(descripcion="     ")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "La descripción es obligatoria.")
        self.assertEqual(self.contar("reporte"), 0)

    # ---------- CA-03: Ubicación válida ----------
    def test_cp05_ubicacion_no_numerica_rechazada(self):
        """CP-05 (CA-03): ubicación no numérica es rechazada"""
        resp = self.enviar(latitud="abc")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["campo"], "ubicacion")
        self.assertEqual(self.contar("reporte"), 0)

    def test_cp06_ubicacion_fuera_de_arequipa_rechazada(self):
        """CP-06 (CA-03): ubicación fuera del área de Arequipa es rechazada"""
        resp = self.enviar(latitud="-12.0464", longitud="-77.0428")  # Lima
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "La ubicación debe estar dentro del área de Arequipa.")
        self.assertEqual(self.contar("reporte"), 0)

    # ---------- CA-04: Foto obligatoria y en formato permitido ----------
    def test_cp07_foto_ausente_rechazada(self):
        """CP-07 (CA-04): reporte sin fotografía es rechazado"""
        datos = self.datos_validos()
        del datos["foto"]
        resp = self.cliente.post("/api/reportes", data=datos, content_type="multipart/form-data")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "La fotografía es obligatoria.")
        self.assertEqual(self.contar("reporte"), 0)

    def test_cp08_formato_de_foto_no_permitido_rechazado(self):
        """CP-08 (CA-04): archivo que no es JPG o PNG es rechazado"""
        resp = self.enviar(foto=(io.BytesIO(b"MZ contenido ejecutable"), "virus.exe"))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "Formato de fotografía no permitido. Use JPG o PNG.")
        self.assertEqual(self.contar("reporte"), 0)
        self.assertEqual(len(self.fotos_guardadas()), 0)

    # ---------- CA-05: Error de persistencia ----------
    def test_cp09_base_de_datos_no_disponible(self):
        """CP-09 (CA-05): con la BD caída se informa el error y no se confirma el registro"""
        self.app.pmv1.db.path = os.path.join(self.carpeta, "carpeta_inexistente", "pmv1.db")
        resp = self.enviar()
        self.assertEqual(resp.status_code, 503)
        cuerpo = resp.get_json()
        self.assertNotIn("id", cuerpo)
        self.assertNotIn("codigo_caso", cuerpo)
        self.assertEqual(cuerpo["error"], "La operación no pudo completarse. Intente nuevamente más tarde.")
        self.assertEqual(len(self.fotos_guardadas()), 0, "no debe quedar una foto huérfana")

    # ---------- CA-06: Tipo de barrera del catálogo ----------
    def test_cp10_tipo_de_barrera_inexistente_rechazado(self):
        """CP-10 (CA-06): tipo de barrera fuera del catálogo es rechazado"""
        resp = self.enviar(id_tipo="99")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()["error"], "Seleccione un tipo de barrera válido.")
        self.assertEqual(self.contar("reporte"), 0)


if __name__ == "__main__":
    unittest.main()
