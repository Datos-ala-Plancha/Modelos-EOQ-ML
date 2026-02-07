# AGENTS.md - Pautas del Proyecto PYMESML

Este archivo proporciona pautas y comandos para agentes de codificación que operan en este repositorio.

# Instrucciones para el Asistente
* empieza siempre tu respuesta con el emoji 🤖
* responde siempre en español
* * no uses en tu codigo ninguna otra variable que no este en la lista anterior salvo que la hayas definido tu mismo en el codigo que generes
* 
## Comandos de Construcción, Lint y Pruebas

### Ejecutar la Aplicación
```bash
streamlit run app/app.py
```

### Ejecutar Pruebas
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar un solo archivo de pruebas
pytest tests/test_gestion_stock.py

# Ejecutar una sola prueba
pytest tests/test_gestion_stock.py::TestEOQClasico::test_eoq_clasico_formula_correcta

# Ejecutar con salida detallada
pytest -v

# Ejecutar con cobertura
pytest --cov=src --cov-report=term-missing
```

### Calidad del Código
```bash
# Verificar formato del código (si ruff está instalado)
ruff check src/ tests/

# Formatear código
ruff format src/ tests/
```

## Pautas de Estilo de Código

### Importaciones
- Usar importaciones absolutas: `from src.models.gestion_stock import GestorStock`
- Agrupar importaciones en este orden: biblioteca estándar, terceros, módulos locales
- Separar grupos con líneas en blanco
```python
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Optional, Union
from dataclasses import dataclass
```

### Formato
- Longitud máxima de línea: 100 caracteres
- Usar 4 espacios para indentación (sin tabs)
- Usar líneas en blanco con moderación para separar secciones lógicas
- Sin espacios en blanco al final
- Usar formato estilo Black (ruff lo exigirá)

### Sugerencias de Tipos
- Usar type hints para todos los parámetros de funciones y valores de retorno
- Usar `Optional[T]` en lugar de `Union[T, None]`
- Usar `Tuple[T1, T2]` para tuplas de longitud fija
- Tipos complejos deben usar `Union` para múltiples opciones
```python
def procesar_datos(df: pd.DataFrame, umbral: float) -> Tuple[pd.DataFrame, Dict[str, float]]:
```

### Convenciones de Nombres
- **Clases**: PascalCase (ej., `GestorStock`, `EOQResult`)
- **Funciones/Variables**: snake_case (ej., `calcular_eoq`, `costo_total`)
- **Constantes**: UPPER_SNAKE_CASE (ej., `DIAS_POR_AÑO`)
- **Métodos privados**: prefijar con `_` (ej., `_validar_parametros`)
- **Variables de tipo**: PascalCase (ej., `T`, `K`, `V`)

### Manejo de Errores
- Usar mensajes de error personalizados en excepciones
- Lanzar `ValueError` para parámetros inválidos
- Capturar excepciones específicas, evitar `except:` sin más
- Usar bloques `try/except` con mensajes de error significativos
```python
if D <= 0:
    raise ValueError("La demanda (D) debe ser positiva")
```

### Docstrings
- Usar comillas triples dobles para docstrings
- Incluir parámetros y tipos de retorno
- Usar español (consistente con el código base)
```python
def eoq_clasico(
    D: float,
    C1: float,
    C3: float,
    C4: float = 0,
    lead_time_dias: float = 0,
) -> EOQResult:
    """
    Modelo EOQ clásico de cantidad económica de pedido

    Parámetros:
    D: Demanda anual (unidades/año)
    C1: Costo de almacenamiento por unidad por año
    C3: Costo de ordenamiento por pedido
    C4: Costo unitario de compra (opcional)
    lead_time_dias: Tiempo de entrega en días
    """
```

### Clases de Datos
- Usar `@dataclass` para contenedores de datos simples
- Definir valores por defecto para campos opcionales
```python
@dataclass
class EOQResult:
    Q_optimo: float
    costo_total: float
    costo_ordenamiento: float
    costo_mantenimiento: float
    numero_pedidos: float
    ciclo_dias: float
    punto_reorden: float = 0.0
```

### Estructura del Proyecto
```
PYMESML/
├── app/           # Aplicación Streamlit
├── src/           # Código fuente
│   ├── models/    # Modelos ML y lógica de negocio
│   ├── data/      # Pipeline de procesamiento de datos
│   └── utils/     # Funciones de utilidad
├── tests/         # Pruebas unitarias
├── data/          # Directorios de datos
├── models/        # Modelos guardados
└── docs/          # Documentación
```

### Flujo de Git
- Crear mensajes de commit significativos
- Hacer commits pequeños y enfocados
- Nunca hacer commit directamente a main sin revisión
- Ejecutar pruebas antes de hacer commit
