"""Adaptador de entrada web (Flask). Traduce HTTP a llamadas al caso de uso (versión 0.1)."""
from flask import Blueprint, jsonify, render_template, request

from app.domain.errores import ValidacionError
from app.domain.reporte import TIPOS_BARRERA, FotoAdjunta
from app.domain.validaciones import SolicitudRegistro


def crear_blueprint(caso_uso_registrar, repositorio):
    bp = Blueprint("reportes", __name__, template_folder="templates")

    @bp.get("/")
    def formulario():
        return render_template("formulario.html", tipos=TIPOS_BARRERA)

    @bp.post("/api/reportes")
    def registrar():
        archivo = request.files.get("foto")
        foto = None
        if archivo is not None and archivo.filename:
            foto = FotoAdjunta(archivo.filename, archivo.read())
        solicitud = SolicitudRegistro(
            id_tipo=request.form.get("id_tipo"),
            descripcion=request.form.get("descripcion"),
            latitud=request.form.get("latitud"),
            longitud=request.form.get("longitud"),
            foto=foto,
            canal="WEB",
        )
        try:
            reporte = caso_uso_registrar.ejecutar(solicitud)
        except ValidacionError as error:
            return jsonify({"error": error.mensaje, "campo": error.campo}), 400
        return jsonify({
            "id": reporte.id_reporte,
            "codigo_caso": reporte.codigo_caso,
            "estado": reporte.estado.value,
        }), 201

    @bp.get("/api/reportes/<int:id_reporte>")
    def consultar(id_reporte):
        reporte = repositorio.obtener(id_reporte)
        if reporte is None:
            return jsonify({"error": "Reporte no encontrado."}), 404
        return jsonify({
            "id": reporte.id_reporte,
            "codigo_caso": reporte.codigo_caso,
            "tipo_barrera": TIPOS_BARRERA[reporte.id_tipo],
            "descripcion": reporte.descripcion,
            "latitud": reporte.latitud,
            "longitud": reporte.longitud,
            "estado": reporte.estado.value,
            "canal": reporte.canal,
            "fecha_creacion": reporte.fecha_creacion,
        })

    return bp
