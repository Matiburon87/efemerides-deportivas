#!/usr/bin/env python3
"""
Script para actualizar la base de datos curada de efemerides.
Lee datos de fuentes web y almacena en efemerides_data.json.
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import date, datetime
from pathlib import Path

# --- CONFIGURACIÓN ---
BASE = Path(__file__).parent / "data"
DATA_FILE = BASE / "efemerides_data.json"
LOG_FILE = BASE / "ultima_actualizacion.log"

# Fuentes para scraping
FUENTES = [
    "https://www.afa.com.ar/884/posts/categories/efemerides",
    "https://www.efemeridesfutboleras.com.ar/",
    "https://www.bhinfo.com.ar/",
    "https://www.lacapital.com.ar/ovacion/",
]


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ts}] {msg}"
    print(linea)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def cargar_datos():
    if not DATA_FILE.exists():
        return {"info": {}, "deportes": {}, "fechas": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def obtener_fuente(url):
    """Intenta obtener el contenido de una URL"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log(f"Error al obtener {url}: {e}")
        return None


def extraer_fechas_del_texto(texto, fecha_buscar):
    """Intenta extraer información relevante para una fecha específica del texto"""
    resultados = []
    # Búsqueda básica de patrones
    patrones = [
        (r"(\d{1,2}) de (\w+) de (\d{4})", "fecha"),
        (r"Naci[oó] ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", "nacimiento"),
        (r"Falleci[oó] ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", "fallecimiento"),
    ]
    return resultados


def actualizar_fecha(fecha_str, datos_extra):
    """Agrega datos extra para una fecha específica"""
    datos = cargar_datos()
    if "fechas" not in datos:
        datos["fechas"] = {}

    if fecha_str not in datos["fechas"]:
        datos["fechas"][fecha_str] = {
            "resumen": f"Efemérides deportivas del {fecha_str}",
            "deportes": {}
        }

    for deporte, items in datos_extra.items():
        if deporte not in datos["fechas"][fecha_str]:
            datos["fechas"][fecha_str][deporte] = {
                "nacimientos": [],
                "fallecimientos": [],
                "hechos": []
            }
        for item in items:
            if item["tipo"] == "nacimiento":
                datos["fechas"][fecha_str][deporte]["nacimientos"].append(item)
            elif item["tipo"] == "fallecimiento":
                datos["fechas"][fecha_str][deporte]["fallecimientos"].append(item)
            elif item["tipo"] == "hecho":
                datos["fechas"][fecha_str][deporte]["hechos"].append(item)

    guardar_datos(datos)
    log(f"Actualizado {fecha_str}: {sum(len(v.get('nacimientos',[])) + len(v.get('fallecimientos',[])) + len(v.get('hechos',[])) for v in datos['fechas'][fecha_str].values())} items nuevos")


def main():
    log("Actualizando base de datos de efemerides...")
    datos = cargar_datos()
    deportes = datos.get("deportes", {})
    log(f"Deportes registrados: {list(deportes.keys())}")

    # Ejemplo: actualizar una fecha específica pasada como argumento
    if len(sys.argv) > 2:
        fecha_str = sys.argv[1]
        deporte = sys.argv[2]
        tipo = sys.argv[3]  # nacimiento, fallecimiento, hecho
        nombre = sys.argv[4]
        detalle = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else ""

        item = {
            "tipo": tipo,
            "nombre": nombre,
            "detalle": detalle,
            "ano": None,
        }
        if len(sys.argv) > 6:
            item["ano"] = int(sys.argv[6])

        datos_extra = {deporte: [item]}
        actualizar_fecha(fecha_str, datos_extra)

    log("Listo.")


if __name__ == "__main__":
    main()