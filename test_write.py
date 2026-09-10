import json

data = {
  "info": {
    "descripcion": "Base de datos curada de efemerides deportivas argentinas",
    "version": "1.0"
  },
  "deportes": {
    "futbol": {"icono": "⚽", "nombre": "Fútbol Argentino"}
  },
  "fechas": {
    "09-10": {
      "resumen": "Efemérides deportivas argentinas del 10 de septiembre",
      "futbol": {
        "nacimientos": [
          {"nombre": "Carlos Tevez", "ano": 1984, "detalle": "Exfutbolista argentino campeón mundial 2022 con Argentina.", "equipo": "Internacional"}
        ],
        "fallecimientos": [
          {"nombre": "Juan Sebastián Veron", "ano": 2025, "detalle": "Exfutbolista argentino, excomodín de la selección y del Manchester United.", "equipo": "Boca Juniors"}
        ],
        "hechos": [
          {"evento": "2026", "detalle": "Mundial de Fútbol en USA/Canada/Mexico.", "importancia": "alto"}
        ]
      }
    }
  }
}

Path = "/c/Users/Win10/Escritorio 2023/Programar/Magic Solutions/saquedemetamdp/efemerides/data/efemerides_data.json"
Path2 = "/c/Users/Win10/Escritorio 2023/Programar/Magic Solutions/saquedemetamdp/efemerides/hoy.json"

# Escribir el archivo JSON correctamente
with open(Path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Archivo escrito: {Path}")
print(f"✅ Contenido: {json.dumps(data, indent=2, ensure_ascii=False)}")