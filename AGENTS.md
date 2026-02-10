# AGENTS.md - Pautas del Proyecto PYMESML

Este archivo proporciona pautas y comandos para agentes de codificación que operan en este repositorio.

## Comandos de Construcción, Lint y Pruebas

### Ejecutar la Aplicación Streamlit
```bash
streamlit run app/app.py
```

### Ejecutar Agente CLI (IO)
```bash
python agent.py
```

### Ejecutar Agente EDA
```bash
python eda_agent.py
```

### Verificar Código
```bash
# Verificar sintaxis Python
python -m py_compile app/app.py
python -m py_compile src/pipelines/*.py

# Verificar imports
python -c "from src.pipelines.business import GestorStockPipeline; from src.pipelines.ml import MLPipeline; print('Imports OK')"
```

## Estructura del Proyecto

```
PYMESML/
├── app/
│   └── app.py              # Aplicación Streamlit
├── src/
│   └── pipelines/          # Pipelines modulares
│       ├── business.py      # GestorStockPipeline
│       └── ml.py          # MLPipeline, PredictorDemandaPipeline
├── agent.py              # Agente conversacional CLI (IO)
├── eda_agent.py          # Agente de EDA
├── .streamlit/
│   └── config.toml       # Configuración
├── requirements.txt
└── README.md
```

## Reglas para Agentes

### Importaciones
- Usar imports absolutos: `from src.pipelines.business import GestorStockPipeline`
- Agrupar importaciones: biblioteca estándar, terceros, locales

### Estilo de Código
- Longitud máxima de línea: 100 caracteres
- Usar 4 espacios para indentación
- Docstrings en español

### Convenciones de Nombres
- Clases: PascalCase
- Funciones/Variables: snake_case
- Constantes: UPPER_SNAKE_CASE

### Manejo de Errores
- Usar mensajes de error personalizados
- ValueError para parámetros inválidos

## Documentación de Agentes

### Agent CLI (agent.py)
```
Comandos disponibles:
/eoq              → EOQ clásico
/eoq_faltantes    → EOQ con backorders
/eoq_descuentos   → EOQ con descuentos
/eoq_produccion   → EOQ de producción
/abc              → Clasificación ABC
/generar          → Generar datos sintéticos
/predecir         → Entrenar modelo ML
/ayuda            → Mostrar ayuda
/salir            → Terminar
```

### EDA Agent (eda_agent.py)
```
Comandos disponibles:
/cargar           → Cargar dataset (CSV, Excel, JSON)
/info             → Información del dataset
/head             → Primeras filas
/tail             → Últimas filas
/shape            → Dimensiones
/dtypes           → Tipos de datos
/describe         → Estadísticas descriptivas
/nulos            → Valores faltantes
/correlacion      → Matriz de correlación
/outliers         → Detectar atípicos
/hist             → Histograma
/boxplot          → Boxplot
/scatter          → Gráfico dispersión
/categorico       → Análisis categórico
/resumen          → EDA completo
/ayuda            → Mostrar ayuda
/salir            → Terminar
```

## Modelos EOQ Implementados

### GestorStockPipeline
```python
from src.pipelines.business import GestorStockPipeline

# EOQ Clásico
r = GestorStockPipeline.eoq_clasico(D, C1, C3, C4, lead)

# EOQ Faltantes
r = GestorStockPipeline.eoq_faltantes(D, C1, C2, C3)

# EOQ Descuentos
rangos = [{"min": 0, "max": 199, "precio": 4000}]
r = GestorStockPipeline.eoq_descuentos(D, C3, i, rangos)

# EOQ Producción
r = GestorStockPipeline.eoq_produccion(D, C1, C3, d, p)

# Clasificación ABC
df, stats = GestorStockPipeline.abc(data, columna, umbral_a, umbral_b)
```

### MLPipeline
```python
from src.pipelines.ml import MLPipeline

# Crear y entrenar
pipeline = MLPipeline("rf")
pipeline.entrenar(X, y)

# Predecir
pipeline.predecir([100, 1, 4])

# Importancia
pipeline.importancia()
```

## Flujo de Git
- Commits pequeños y enfocados
- Mensajes descriptivos
- Tests antes de commit
