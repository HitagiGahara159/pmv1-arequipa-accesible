-- Modelo de datos inicial del PMV1 - Arequipa Accesible (SQLite)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tipo_barrera (
    id_tipo   INTEGER PRIMARY KEY,
    nombre    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS reporte (
    id_reporte      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tipo         INTEGER NOT NULL REFERENCES tipo_barrera(id_tipo),
    canal           TEXT NOT NULL CHECK (canal IN ('WEB', 'WHATSAPP')),
    descripcion     TEXT NOT NULL CHECK (length(trim(descripcion)) > 0),
    latitud         REAL NOT NULL,
    longitud        REAL NOT NULL,
    foto_ruta       TEXT NOT NULL,
    estado          TEXT NOT NULL DEFAULT 'PENDIENTE'
                    CHECK (estado IN ('PENDIENTE', 'REVISADO', 'DERIVADO', 'ATENDIDO')),
    fecha_creacion  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS historial_estado (
    id_historial  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reporte    INTEGER NOT NULL REFERENCES reporte(id_reporte),
    estado        TEXT NOT NULL,
    fecha_cambio  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_reporte_estado ON reporte(estado);
CREATE INDEX IF NOT EXISTS idx_reporte_ubicacion ON reporte(latitud, longitud);
