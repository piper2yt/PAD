#!/usr/bin/env python3
"""Construye la base de datos local SQLite a partir de los CSV en `data/`.

Este script busca automáticamente todos los archivos `.csv` dentro de la carpeta
`data/` y los carga por bloques (chunks) en `data/proyecto.sqlite` para evitar
problemas de memoria RAM al trabajar con datasets grandes como
"Financial Transactions Dataset: Analytics" de Kaggle.

Uso básico (desde la raíz del repositorio):
    python src/crear_db.py

Uso avanzado con parámetros opcionales:
    python src/crear_db.py --chunksize 50000 --crear-indices
"""

from __future__ import annotations

import argparse
import logging
import re
import sqlite3
import sys
import time
from pathlib import Path

import pandas as pd

# Rutas predeterminadas basadas en la ubicación del repositorio
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DB_PATH = DEFAULT_DATA_DIR / "proyecto.sqlite"
DEFAULT_CHUNKSIZE = 100_000

# Columnas frecuentes en el dataset para creación opcional de índices
SUGGESTED_INDEX_COLUMNS = ("id", "client_id", "card_id", "date", "mcc")

KAGGLE_DATASET_URL = (
    "https://www.kaggle.com/datasets/computingvictor/"
    "transactions-fraud-datasets?resource=download"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def sanitizar_nombre_tabla(ruta_csv: Path) -> str:
    """Genera un nombre de tabla seguro para SQLite a partir del nombre del CSV."""
    nombre = re.sub(r"[^a-zA-Z0-9_]+", "_", ruta_csv.stem.strip().lower()).strip("_")
    if not nombre:
        nombre = "tabla"
    if nombre[0].isdigit():
        nombre = f"t_{nombre}"
    return nombre


def sanitizar_columnas(columnas: pd.Index) -> list[str]:
    """Limpia espacios en los encabezados del CSV manteniendo nombres legibles."""
    limpias: list[str] = []
    vistas: dict[str, int] = {}

    for indice, col in enumerate(columnas):
        nombre = re.sub(r"\s+", "_", str(col).strip())
        if not nombre:
            nombre = f"col_{indice}"
        conteo = vistas.get(nombre, 0)
        vistas[nombre] = conteo + 1
        if conteo > 0:
            nombre = f"{nombre}_{conteo}"
        limpias.append(nombre)

    return limpias


def cargar_csv_a_sqlite(
    ruta_csv: Path,
    conexion: sqlite3.Connection,
    chunksize: int,
    nombre_tabla: str | None = None,
) -> tuple[str, int]:
    """Carga un archivo CSV en SQLite por bloques para controlar el uso de memoria."""
    tabla = nombre_tabla or sanitizar_nombre_tabla(ruta_csv)
    tamano_mb = ruta_csv.stat().st_size / (1024 * 1024)
    logger.info(
        "Procesando '%s' (%.2f MB) -> tabla '%s' (bloques de %s filas)...",
        ruta_csv.name,
        tamano_mb,
        tabla,
        f"{chunksize:,}",
    )

    inicio = time.perf_counter()
    total_filas = 0
    columnas_limpias: list[str] | None = None

    with pd.read_csv(ruta_csv, chunksize=chunksize, low_memory=False) as lector:
        for num_bloque, bloque in enumerate(lector, start=1):
            if columnas_limpias is None:
                columnas_limpias = sanitizar_columnas(bloque.columns)
            bloque.columns = columnas_limpias

            modo_escritura = "replace" if num_bloque == 1 else "append"
            bloque.to_sql(
                name=tabla,
                con=conexion,
                if_exists=modo_escritura,
                index=False,
            )

            total_filas += len(bloque)
            transcurrido = time.perf_counter() - inicio
            logger.info(
                "  [%s] Bloque %d cargado | filas acumuladas: %s (%.1fs)",
                tabla,
                num_bloque,
                f"{total_filas:,}",
                transcurrido,
            )

    # Caso borde: CSV que solo contiene encabezados sin filas de datos
    if total_filas == 0:
        vacio = pd.read_csv(ruta_csv, nrows=0)
        vacio.columns = sanitizar_columnas(vacio.columns)
        vacio.to_sql(name=tabla, con=conexion, if_exists="replace", index=False)
        logger.warning(
            "  [%s] El archivo no contenía filas; se creó la tabla vacía con su esquema.",
            tabla,
        )

    duracion = time.perf_counter() - inicio
    logger.info(
        "Finalizada tabla '%s': %s filas cargadas en %.2f segundos.",
        tabla,
        f"{total_filas:,}",
        duracion,
    )
    return tabla, total_filas


def crear_indices_sugeridos(conexion: sqlite3.Connection, nombre_tabla: str) -> None:
    """Crea índices sobre columnas clave frecuentes si existen en la tabla."""
    cursor = conexion.cursor()
    columnas_tabla = {
        fila[1] for fila in cursor.execute(f'PRAGMA table_info("{nombre_tabla}")').fetchall()
    }
    columnas_indexables = [c for c in SUGGESTED_INDEX_COLUMNS if c in columnas_tabla]

    for columna in columnas_indexables:
        nombre_indice = f"idx_{nombre_tabla}_{columna}"
        logger.info("Creando índice '%s' en %s(%s)...", nombre_indice, nombre_tabla, columna)
        cursor.execute(
            f'CREATE INDEX IF NOT EXISTS "{nombre_indice}" '
            f'ON "{nombre_tabla}" ("{columna}")'
        )
    conexion.commit()


def mostrar_resumen_db(conexion: sqlite3.Connection, ruta_db: Path) -> None:
    """Muestra un resumen final de las tablas disponibles y el tamaño de la BD."""
    cursor = conexion.cursor()
    tablas = [
        fila[0]
        for fila in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    ]

    logger.info("=" * 60)
    logger.info("RESUMEN DE LA BASE DE DATOS: %s", ruta_db)
    logger.info("-" * 60)
    for tabla in tablas:
        conteo = cursor.execute(f'SELECT COUNT(*) FROM "{tabla}"').fetchone()[0]
        logger.info("  %-25s : %12s filas", tabla, f"{conteo:,}")
    tamano_db_mb = ruta_db.stat().st_size / (1024 * 1024)
    logger.info("-" * 60)
    logger.info("Tamaño total en disco: %.2f MB", tamano_db_mb)
    logger.info("=" * 60)


def construir_base_datos(
    data_dir: Path,
    db_path: Path,
    chunksize: int,
    crear_indices: bool = False,
) -> int:
    """Orquesta la detección de archivos CSV y su ingesta en SQLite."""
    if chunksize <= 0:
        logger.error("El parámetro --chunksize debe ser un número entero positivo.")
        return 1

    if not data_dir.exists():
        logger.error("La carpeta de datos no existe: %s", data_dir)
        return 1

    archivos_csv = sorted(
        ruta for ruta in data_dir.glob("*.csv") if ruta.is_file() and not ruta.name.startswith(".")
    )

    if not archivos_csv:
        logger.warning("No se encontraron archivos .csv en '%s'.", data_dir)
        logger.info(
            "Descarga el dataset desde Kaggle, descomprímelo y coloca los .csv en '%s':\n  %s",
            data_dir,
            KAGGLE_DATASET_URL,
        )
        return 1

    db_path.parent.mkdir(parents=True, exist_ok=True)
    inicio_total = time.perf_counter()

    logger.info(
        "Se encontraron %d archivo(s) CSV en '%s': %s",
        len(archivos_csv),
        data_dir,
        ", ".join(p.name for p in archivos_csv),
    )

    tablas_cargadas: list[str] = []
    tablas_usadas: set[str] = set()

    conexion = sqlite3.connect(db_path)
    try:
        # Ajustes de SQLite para acelerar cargas masivas por bloques
        conexion.execute("PRAGMA journal_mode = WAL;")
        conexion.execute("PRAGMA synchronous = NORMAL;")
        conexion.execute("PRAGMA temp_store = MEMORY;")
        conexion.execute("PRAGMA cache_size = -64000;")

        for ruta_csv in archivos_csv:
            nombre_base = sanitizar_nombre_tabla(ruta_csv)
            nombre_tabla = nombre_base
            sufijo = 2
            while nombre_tabla in tablas_usadas:
                nombre_tabla = f"{nombre_base}_{sufijo}"
                sufijo += 1
            tablas_usadas.add(nombre_tabla)

            tabla, _ = cargar_csv_a_sqlite(
                ruta_csv=ruta_csv,
                conexion=conexion,
                chunksize=chunksize,
                nombre_tabla=nombre_tabla,
            )
            tablas_cargadas.append(tabla)

        if crear_indices:
            logger.info("Creando índices sugeridos sobre columnas clave...")
            for tabla in tablas_cargadas:
                crear_indices_sugeridos(conexion, tabla)

        # Consolidar WAL y volver a modo DELETE para dejar un único archivo .sqlite limpio
        conexion.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conexion.execute("PRAGMA journal_mode = DELETE;")
        conexion.commit()

        mostrar_resumen_db(conexion, db_path)
    finally:
        conexion.close()

    duracion_total = time.perf_counter() - inicio_total
    logger.info("Proceso completado exitosamente en %.2f segundos.", duracion_total)
    return 0


def parsear_argumentos() -> argparse.Namespace:
    """Define y procesa los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description=(
            "Carga todos los archivos .csv de data/ por bloques en data/proyecto.sqlite."
        )
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help=f"Carpeta donde se encuentran los archivos CSV (por defecto: {DEFAULT_DATA_DIR}).",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Ruta de la base de datos SQLite de salida (por defecto: {DEFAULT_DB_PATH}).",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=DEFAULT_CHUNKSIZE,
        help=f"Número de filas por bloque al leer cada CSV (por defecto: {DEFAULT_CHUNKSIZE:,}).",
    )
    parser.add_argument(
        "--crear-indices",
        action="store_true",
        help="Crea índices básicos en columnas clave (id, client_id, card_id, date, mcc).",
    )
    return parser.parse_args()


def main() -> int:
    """Punto de entrada principal del script."""
    args = parsear_argumentos()
    return construir_base_datos(
        data_dir=args.data_dir,
        db_path=args.db_path,
        chunksize=args.chunksize,
        crear_indices=args.crear_indices,
    )


if __name__ == "__main__":
    sys.exit(main())
