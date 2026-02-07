# PYMESML - Aplicación de Investigación Operativa

Aplicación web de gestión de inventarios y predicción de demanda, diseñada con arquitectura de pipelines modulares para maximizar la mantenibilidad y escalabilidad.

## Características

### Gestión de Stock - Modelos EOQ
| Modelo | Descripción |
|--------|-------------|
| **EOQ Clásico** | Cantidad económica de pedido tradicional |
| **EOQ Faltantes** | Modelo con backorders permitidos |
| **EOQ Descuentos** | Análisis de descuentos por volumen |
| **EOQ Producción** | Optimización para producción interna |
| **Clasificación ABC** | Identificación de productos críticos (Pareto) |

### Predicción de Demanda
- Generación de series temporales sintéticas
- Modelos ML: Lineal, Ridge, Random Forest, Gradient Boosting
- Métricas: R², RMSE, MAE

### Análisis de Datos
- Carga de datasets CSV
- Estadísticas descriptivas
- Visualizaciones: histogramas, boxplots, dispersión
- Matriz de correlación

## Arquitectura

```
PYMESML/
├── app/
│   └── app.py              # Interfaz Streamlit
├── src/
│   └── pipelines/          # Pipelines modulares
│       ├── business.py      # Modelos EOQ
│       └── ml.py           # ML Pipeline
├── .streamlit/
│   └── config.toml         # Tema oscuro
├── requirements.txt
├── README.md
└── LICENSE
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/Kerbero05/PYMESML.git
cd PYMESML

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app/app.py
```

## API de Pipelines

### GestorStockPipeline

```python
from src.pipelines.business import GestorStockPipeline

# EOQ Clásico
resultado = GestorStockPipeline.eoq_clasico(
    D=1000,          # Demanda anual
    C1=2.5,          # Costo almacenamiento
    C3=10,           # Costo ordenamiento
    C4=5,            # Costo unitario (opcional)
    lead=5            # Lead time días (opcional)
)
# Atributos: Q_optimo, costo_total, numero_pedidos, ciclo_dias, punto_reorden

# EOQ con Faltantes
r = GestorStockPipeline.eoq_faltantes(D, C1, C2, C3)

# EOQ con Descuentos
rangos = [{"min": 0, "max": 199, "precio": 4000}, ...]
r = GestorStockPipeline.eoq_descuentos(D, C3, i, rangos)

# EOQ Producción
r = GestorStockPipeline.eoq_produccion(D, C1, C3, d, p)

# Clasificación ABC
df_clasificado, stats = GestorStockPipeline.abc(df, "valor", 0.8, 0.95)
```

### MLPipeline

```python
from src.pipelines.ml import MLPipeline

# Crear modelo (lineal, ridge, rf, gb)
pipeline = MLPipeline("rf")

# Entrenar
metricas = pipeline.entrenar(X, y)

# Predecir
prediccion = pipeline.predecir([100, 1, 4])

# Importancia de características
importancia = pipeline.importancia()
```

### PredictorDemandaPipeline

```python
from src.pipelines.ml import PredictorDemandaPipeline

# Generar datos sintéticos
df = PredictorDemandaPipeline.generar(
    n=365,           # Días
    tendencia=0.5,
    estacional=15,
    ruido=5,
    base=100
)

# Promedio móvil
movil = PredictorDemandaPipeline.movils(serie, ventana=7)

# Descomponer serie
tendencia, estacionalidad, residuo = PredictorDemandaPipeline.descomponer(serie)
```

## Tecnologías

| Tecnología | Propósito |
|-----------|-----------|
| **Streamlit** | Interfaz web interactiva |
| **NumPy** | Cálculos numéricos |
| **Pandas** | Manipulación de datos |
| **Scikit-learn** | Machine Learning |
| **Plotly** | Gráficos interactivos |
| **Matplotlib** | Gráficos estáticos |

## Autor

 kerbero05

## Licencia

MIT License

Copyright (c) 2026 kerbero05

Ver archivo [LICENSE](LICENSE) para más detalles.
