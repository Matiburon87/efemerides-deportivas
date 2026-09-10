#!/usr/bin/env python3
"""
Generador simplificado de efemerides para probar el sistema.
Solo lee los datos curados y genera hoy.json para GitHub Pages.
"""

import json
from datetime import date, datetime
from pathlib import Path

# Configuración
BASE = Path(r"F:\Escritorio 2023\Programar\Magic Solutions\saquedemetamdp\efemerides")
DATA_FILE = BASE / "data" / "efemerides_data.json"
OUTPUT_FILE = BASE / "hoy.json"
LOG_FILE = BASE / "ultima_prueba.log"

# Iconos por deporte
ICONOS = {
    "futbol": "⚽", "basquet": "🏀", "tenis": "🎾",
    "racing": "🏎️", "rugby": "🏉", "beisbol": "⚾",
    "patinaje": "⛸️", "boxeo": "🥊", "ciclismo": "🚴",
    "handball": "🤾", "futbol_femenino": "👩‍🦰"
}

DEPORTES_ORDEN = [
    "futbol", "basquet", "tenis", "racing", "rugby",
    "beisbol", "patinaje", "boxeo", "ciclismo", "handball", "futbol_femenino"
]


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


def cargar_datos():
    if not DATA_FILE.exists():
        log(f"ERROR: No se encontró {DATA_FILE}")
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def formatear_fecha(fecha_str):
    try:
        dt = datetime.strptime(fecha_str, "%Y-%m-%d")
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return f"{dt.day} de {meses[dt.month - 1]} de {dt.year}"
    except Exception:
        return fecha_str


def generar_json(fecha_str=None):
    if fecha_str is None:
        fecha_str = date.today().strftime("%Y-%m-%d")

    log(f"Generando efemerides para {fecha_str}...")

    datos = cargar_datos()
    fechas_data = datos.get("fechas", {})
    deportes_info = datos.get("deportes", {})

    fecha_key = "-".join(fecha_str.split("-")[1:])  # MM-DD
    info_fecha = fechas_data.get(fecha_key, {})

    hoy = {
        "fecha": fecha_str,
        "fecha_formateada": formatear_fecha(fecha_str),
        "resumen": info_fecha.get("resumen", f"Efemérides deportivas argentinas del {formatear_fecha(fecha_str)}"),
        "total_items": 0,
        "deportes": {}
    }

    for deporte in DEPORTES_ORDEN:
        data_deporte = info_fecha.get(deporte, {})
        if not data_deporte:
            continue

        nacimientos = data_deporte.get("nacimientos", [])
        fallecimientos = data_deporte.get("fallecimientos", [])
        hechos = data_deporte.get("hechos", [])

        if nacimientos or fallecimientos or hechos:
            hoy["deportes"][deporte] = {
                "icono": ICONOS.get(deporte, "⚽"),
                "nombre": deportes_info.get(deporte, {}).get("nombre", deporte),
                "nacimientos": nacimientos,
                "fallecimientos": fallecimientos,
                "hechos": hechos,
            }
            hoy["total_items"] += len(nacimientos) + len(fallecimientos) + len(hechos)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(hoy, f, ensure_ascii=False, indent=2)

    log(f"✓ Generado: {OUTPUT_FILE}")
    log(f"  Total items: {hoy['total_items']} en {len(hoy['deportes'])} deportes")

    for deporte, info in hoy["deportes"].items():
        log(f"    {info['icono']} {info['nombre']}: "
            f"{len(info['nacimientos'])} nac, "
            f"{len(info['fallecimientos'])} falle, "
            f"{len(info['hechos'])} hechos")

    return hoy


if __name__ == "__main__":
    import sys
    fecha_arg = sys.argv[1] if len(sys.argv) > 1 else None
    resultado = generar_json(fecha_arg)
    print("\n✅ JSON generado correctamente.")