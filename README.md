# PMV1 - Arequipa Accesible

Producto Mínimo Viable 1 del proyecto **Arequipa Accesible**: plataforma para que los ciudadanos
reporten barreras de accesibilidad urbana en Arequipa (web + WhatsApp, con IA en incrementos posteriores).

**Funcionalidad implementada (HU-01):** registrar un reporte de barrera con fotografía, tipo,
ubicación y descripción, guardado en base de datos con estado `PENDIENTE` y número de caso.

## Arquitectura

Arquitectura **hexagonal** (puertos y adaptadores):

```
app/
├── domain/         entidades y reglas de validación (sin dependencias externas)
├── application/    casos de uso (registrar_reporte.py)
├── ports/          contratos: ReporteRepository, FotoStorage
├── adapters/
│   ├── entrada/    adaptador web (Flask) -> a futuro: webhook de WhatsApp
│   └── salida/     repositorio SQLite, almacén local de fotos
└── infrastructure/ configuración y conexión a la base de datos
```
Diagramas PlantUML en `docs/`.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # ajustar valores si hace falta
```

## Ejecución

```bash
python main.py
```
Abrir http://127.0.0.1:5000 para usar el formulario de nuevo reporte.

### Registrar un reporte por API
```bash
curl -X POST http://127.0.0.1:5000/api/reportes \
  -F id_tipo=2 -F descripcion="No hay rampa frente al hospital" \
  -F latitud=-16.3989 -F longitud=-71.5350 -F foto=@foto.png
```
Respuesta esperada (201): `{"codigo_caso":"AQP-000001","estado":"PENDIENTE","id":1}`

## Pruebas

```bash
python -m unittest discover -s tests -v
```
Cada prueba (CP) está vinculada a un criterio de aceptación (CA) de la historia HU-01.

## Flujo de trabajo con Git

```bash
git switch -c feature/nombre-de-la-historia
# implementar y probar
git add . && git commit -m "feat: descripción corta"
git push -u origin feature/nombre-de-la-historia   # luego abrir un Pull Request
```
Convención de commits: `feat`, `fix`, `test`, `docs`, `chore`.

## Seguridad
No subir `.env`, bases de datos (`*.db`) ni la carpeta `uploads/`; están en `.gitignore`.
