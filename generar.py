#!/usr/bin/env python3
"""
Generador diario de efemerides deportivas argentinas.
Lee datos curados, busca en web fuentes abiertas, y genera hoy.json.
Sube a GitHub Pages si está configurado.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

# --- CONFIGURACIÓN ---
BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "efemerides_data.json"
OUTPUT_FILE = BASE / "hoy.json"
LOG_FILE = BASE / "ultima_ejecucion.log"

# Fuentes para buscar datos adicionales
FUENTES_WEB = [
    "https://www.efemeridesfutboleras.com.ar/",
    "https://www.bhinfo.com.ar/",
    "https://www.lacapital.com.ar/ovacion/",
]

# Deportes ordenados por prioridad
DEPORTES_ORDEN = [
    "futbol", "basquet", "tenis", "racing", "rugby",
    "beisbol", "patinaje", "boxeo", "ciclismo", "handball", "futbol_femenino"
]

# Icons map (para el JSON de salida, usado por el frontend)
ICONOS = {
    "futbol": "⚽", "basquet": "🏀", "tenis": "🎾",
    "racing": "🏎️", "rugby": "🏉", "beisbol": "⚾",
    "patinaje": "⛸️", "boxeo": "🥊", "ciclismo": "🚴",
    "handball": "🤾", "futbol_femenino": "👩‍🦰"
}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ts}] {msg}"
    print(linea)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def cargar_datos_curados():
    if not DATA_FILE.exists():
        log(f"ADVERTENCIA: No se encontró {DATA_FILE}, usando datos vacíos")
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_fecha_brasilia(fecha_str):
    """Convierte 'AAAA-MM-DD' a 'DD de mes de AAAA' en español"""
    try:
        dt = datetime.strptime(fecha_str, "%Y-%m-%d")
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        return f"{dt.day} de {meses[dt.month - 1]} de {dt.year}"
    except Exception:
        return fecha_str


def buscar_en_fuentes_web(fecha_str):
    """Intenta obtener datos adicionales de fuentes web abiertas"""
    # En producción, aquí iría requests con timeout, user-agent, etc.
    # Por ahora, no hace nada porque requiere configuración extra
    return []


def generar_hoy(fecha_str=None):
    """Genera el JSON del día para GitHub Pages"""
    if fecha_str is None:
        fecha_str = date.today().strftime("%Y-%m-%d")

    log(f"Generando efemerides para {fecha_str}...")

    datos = cargar_datos_curados()
    dias_data = datos.get("fechas", {})
    deportes_info = datos.get("deportes", {})

    fecha_key = "-".join(fecha_str.split("-")[1:])  # MM-DD
    info_fecha = dias_data.get(fecha_key, {})

    # Intenta complementar con web
    extra_web = buscar_en_fuentes_web(fecha_str)

    # Construir estructura
    hoy = {
        "fecha": fecha_str,
        "fecha_formateada": format_fecha_brasilia(fecha_str),
        "resumen": info_fecha.get("resumen", f"Efemérides deportivas argentinas del {format_fecha_brasilia(fecha_str)}"),
        "necesita_actualizacion": not bool(info_fecha),
        "deportes": {},
    }

    for deporte in DEPORTES_ORDEN:
        data_deporte = info_fecha.get(deporte, {})
        if not data_deporte:
            continue

        nacimientos = data_deporte.get("nacimientos", [])
        fallecimientos = data_deporte.get("fallecimientos", [])
        hechos = data_deporte.get("hechos", [])

        # Si hay datos adicionales de web, los agregamos
        if extra_web and deporte == "futbol":
            for item in extra_web:
                if item.get("tipo") == "nacimiento" and item not in nacimientos:
                    nacimientos.append(item)
                elif item.get("tipo") == "fallecimiento" and item not in fallecimientos:
                    fallecimientos.append(item)
                elif item.get("tipo") == "hecho" and item not in hechos:
                    hechos.append(item)

        if nacimientos or fallecimientos or hechos:
            hoy["deportes"][deporte] = {
                "icono": ICONOS.get(deporte, "⚽"),
                "nombre": deportes_info.get(deporte, {}).get("nombre", deporte),
                "nacimientos": nacimientos,
                "fallecimientos": fallecimientos,
                "hechos": hechos,
                "total_items": len(nacimientos) + len(fallecimientos) + len(hechos),
            }

    # Ordenar deportes por total de items (más relevante primero)
    if hoy["deportes"]:
        hoy["deportes"] = dict(
            sorted(hoy["deportes"].items(), key=lambda x: x[1]["total_items"], reverse=True)
        )

    hoy["total_items"] = sum(d["total_items"] for d in hoy["deportes"].values())

    return hoy


def guardar_hoy(hoy_data):
    """Guarda hoy.json"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(hoy_data, f, ensure_ascii=False, indent=2)
    log(f"Guardado: {OUTPUT_FILE} ({len(json.dumps(hoy_data))} bytes)")


def subir_github():
    """Sube hoy.json a GitHub Pages si hay credenciales"""
    # Esta función se implementa cuando el repo está configurado
    log("Push a GitHub: funcionalidad pendiente de configuración del repo.")
    return False


def main(fecha=None):
    """Punto de entrada"""
    log("=" * 60)
    log("Efemerides Deportivas — Generador Diario")
    log("=" * 60)

    hoy = generar_hoy(fecha)
    guardar_hoy(hoy)

    log(f"Resumen: {hoy['total_items']} items en {len(hoy['deportes'])} deportes")
    for deporte, info in hoy["deportes"].items():
        log(f"  {info['icono']} {info['nombre']}: {info['total_items']} items "
            f"({len(info['nacimientos'])} nac, {len(info['fallecimientos'])} falle, {len(info['hechos'])} hechos)")

    if hoy["necesita_actualizacion"]:
        log("⚠️  ADVERTENCIA: Esta fecha no tiene datos en la base curada. Revisar fuentes.")

    log("Listo.")
    return hoy


if __name__ == "__main__":
    fecha_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(fecha_arg)