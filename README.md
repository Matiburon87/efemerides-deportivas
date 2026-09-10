# Sistema de Efemérides Deportivas Argentinas

## 1. ¿Qué es el sistema de efemerides?

El sistema de efemerides es un generador automático de contenido diario que recopila eventos deportivos históricos argentinos (nacimientos, fallecimientos y hechos destacados) y los publica en formato JSON para su consumo por una aplicación web.

### Componentes del sistema

| Componente | Descripción |
|------------|-------------|
| `data/efemerides_data.json` | Base de datos curada con todas las efemérides organizadas por fecha (MM-DD) |
| `generar.py` | Script principal que genera `hoy.json` para el día actual |
| `generar_simple.py` | Versión simplificada del generador para pruebas |
| `actualizar_base.py` | Script para agregar nuevas efemérides a la base de datos curada |
| `hoy.json` | Archivo de salida diario que se sirve vía GitHub Pages |

### Deportes soportados

- ⚽ Fútbol Argentino
- 👩‍🦰 Fútbol Femenino Argentino
- 🏀 Basketball Argentino
- 🎾 Tenis Argentino
- 🏎️ Automovilismo Argentino
- 🏉 Rugby Argentino
- ⚾ Béisbol Argentino
- 🥊 Boxeo Argentino
- 🚴 Ciclismo Argentino
- 🤾 Handball Argentino
- ⛸️ Patinaje Argentino

### Tipos de eventos

Cada deporte puede contener tres tipos de eventos:

- **Nacimientos**: Deportistas nacidos en esa fecha (con año, detalle y equipo)
- **Fallecimientos**: Deportistas fallecidos en esa fecha
- **Hechos**: Eventos históricos destacados (con evento, detalle e importancia)

---

## 2. Cómo ejecutar el generador diario

### Requisitos

- Python 3.7+
- No requiere dependencias externas (solo biblioteca estándar)

### Ejecución del generador principal

```bash
# Generar efemérides para el día actual
python generar.py

# Generar efemérides para una fecha específica (formato: YYYY-MM-DD)
python generar.py 2026-01-01
```

### Ejecución del generador simplificado (para pruebas)

```bash
# Generar para el día actual
python generar_simple.py

# Generar para una fecha específica
python generar_simple.py 2026-01-01
```

### Salida esperada

El generador produce:

1. **`hoy.json`** — Archivo JSON con las efemérides del día
2. **`ultima_ejecucion.log`** — Log con timestamp de la última ejecución

### Estructura del JSON generado

```json
{
  "fecha": "2026-01-01",
  "fecha_formateada": "1 de enero de 2026",
  "resumen": "Año Nuevo. Día de inauguración de la era moderna del deporte argentino.",
  "necesita_actualizacion": false,
  "deportes": {
    "futbol": {
      "icono": "⚽",
      "nombre": "Fútbol Argentino",
      "nacimientos": [...],
      "fallecimientos": [...],
      "hechos": [...]
    }
  },
  "total_items": 5
}
```

---

## 3. Cómo agregar nuevas fechas a la base de datos

### Método 1: Usando `actualizar_base.py` (línea de comandos)

```bash
# Sintaxis:
python actualizar_base.py <fecha> <deporte> <tipo> <nombre> <detalle> [año]

# Ejemplo: agregar nacimiento en fútbol
python actualizar_base.py 01-01 futbol nacimiento "Juan Pérez" "Detalle del jugador" 1990

# Ejemplo: agregar hecho histórico en básquet
python actualizar_base.py 01-01 basquet hecho "Evento histórico" "Descripción del evento"
```

### Método 2: Edición manual de `data/efemerides_data.json`

1. Abrir `data/efemerides_data.json` en un editor de texto
2. Localizar o crear la entrada con la fecha en formato `MM-DD` dentro del objeto `"fechas"`
3. Agregar el deporte con la estructura correspondiente:

```json
{
  "fechas": {
    "MM-DD": {
      "resumen": "Descripción general del día",
      "futbol": {
        "nacimientos": [
          {
            "nombre": "Nombre del deportista",
            "ano": 1990,
            "detalle": "Biografía breve",
            "equipo": "Equipo principal"
          }
        ],
        "fallecimientos": [
          {
            "nombre": "Nombre del deportista",
            "ano": 1950,
            "detalle": "Biografía breve"
          }
        ],
        "hechos": [
          {
            "evento": "Año — Descripción del evento",
            "detalle": "Información adicional",
            "importancia": "alto|medio|bajo"
          }
        ]
      }
    }
  }
}
```

### Convenciones para fechas

- Las fechas se guardan como `"MM-DD"` (ej: `"01-01"` para 1 de enero)
- El año en los eventos es opcional y se usa para nacimientos/fallecimientos
- Los deportes deben coincidir con las claves definidas en `efemerides_data.json` > `"deportes"`

### Validación

Después de editar manualmente, ejecutar el generador para verificar que el JSON se genera correctamente:

```bash
python generar.py
```

---

## 4. Fuentes de datos

### Fuentes web

| Fuente | URL | Descripción |
|--------|-----|-------------|
| Efemérides Futboleras | https://www.efemeridesfutboleras.com.ar/ | Efemérides del fútbol argentino |
| BH Info | https://www.bhinfo.com.ar/ | Historia del deporte argentino |
| La Capital - Ovación | https://www.lacapital.com.ar/ovacion/ | Sección deportiva del diario |
| AFA | https://www.afa.com.ar/884/posts/categories/efemerides | Efemérides oficiales de la AFA |

### Fuentes en redes sociales

| Plataforma | Perfil | ID |
|------------|--------|-----|
| Facebook | Efemérides Deportivas | 100076505384269 |
| Facebook | Efemérides Deportivas | 100090301745960 |
| Facebook | Efemérides Deportivas | 100063797646276 |

### Proceso de curación

1. Revisión diaria de las fuentes web y perfiles de Facebook
2. Extracción de eventos relevantes (nacimientos, fallecimientos, hechos históricos)
3. Verificación cruzada con múltiples fuentes
4. Formato y carga en `data/efemerides_data.json`
5. Generación del `hoy.json` correspondiente

---

## 5. Flujo de trabajo con GitHub Pages

### Repositorio de publicación

- **Repositorio**: `Matiboron87/efemerides-deportivas`
- **URL pública**: `https://Matiboron87.github.io/efemerides-deportivas/`
- **Archivo servido**: `hoy.json`

### Flujo completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE TRABAJO DIARIO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. REVISIÓN DE FUENTES                                          │
│     ├── efemeridesfutboleras.com.ar                              │
│     ├── Perfiles de Facebook                                     │
│     └── Otras fuentes (AFA, BH Info, etc.)                       │
│                                                                  │
│  2. ACTUALIZACIÓN DE BASE                                        │
│     ├── python actualizar_base.py <fecha> <deporte> ...          │
│     └── Edición manual de efemerides_data.json                   │
│                                                                  │
│  3. GENERACIÓN DEL JSON DIARIO                                   │
│     └── python generar.py                                        │
│         └── Genera: hoy.json                                     │
│                                                                  │
│  4. SUBIDA A GITHUB PAGES                                        │
│     ├── git add hoy.json                                         │
│     ├── git commit -m "Efemerides YYYY-MM-DD"                    │
│     └── git push origin main                                     │
│                                                                  │
│  5. CONSUMO POR FRONTEND                                         │
│     └── saquedemeta/src/components/efemerides/EfemeredesHoy.jsx  │
│         └── Fetch: https://Matiboron87.github.io/.../hoy.json   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Configuración del frontend

El componente React `EfemeredesHoy.jsx` consume el JSON desde GitHub Pages:

```javascript
// saquedemeta/src/components/efemerides/EfemeredesHoy.jsx
const URL_EFEMERIDES = "https://Matiboron87.github.io/efemerides-deportivas/hoy.json";

// Fetch y renderizado de efemérides
```

### Automatización sugerida

Para automatizar la generación diaria, se puede configurar:

1. **GitHub Actions**: Workflow programado que ejecute `generar.py` diariamente
2. **Cron job local**: Ejecutar el script y hacer push automático
3. **GitHub API**: Subir directamente a la rama `gh-pages`

---

## Estructura del proyecto

```
efemerides/
├── README.md                  # Este archivo
├── generar.py                 # Generador principal
├── generar_simple.py          # Generador simplificado (pruebas)
├── actualizar_base.py         # Script para actualizar base de datos
├── hoy.json                   # Salida del generador (último día)
├── ultima_ejecucion.log       # Log de la última ejecución
└── data/
    ├── efemerides_data.json   # Base de datos curada (fuente de verdad)
    └── ultima_actualizacion.log # Log de actualizaciones de la base
```

---

## Notas adicionales

- **Idioma**: Todo el contenido está en español
- **Codificación**: UTF-8 (soporte para caracteres especiales como tildes e ñ)
- **Formato de fechas**: ISO 8601 (`YYYY-MM-DD`) para entrada, `MM-DD` como clave interna
- **Logs**: Cada ejecución genera entradas con timestamp para auditoría
- **Consistencia**: El frontend espera la estructura exacta generada por `generar.py`
