# PYMESML - Aplicación de Investigación Operativa

MVP con arquitectura de pipelines modulares.

## Estructura

```
PYMESML/
├── app/app.py              # Aplicación Streamlit
├── src/pipelines/          # Pipelines modulares
│   ├── business.py        # Modelos EOQ
│   └── ml.py             # ML Pipeline
├── .streamlit/config.toml  # Tema oscuro
├── requirements.txt
└── README.md
```

## Instalación

```bash
git clone https://github.com/Kerbero05/PYMESML.git
cd PYMESML
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app/app.py
```

## Pipelines

```python
from src.pipelines.business import GestorStockPipeline
from src.pipelines.ml import MLPipeline, PredictorDemandaPipeline

# EOQ
r = GestorStockPipeline.eoq_clasico(D=1000, C1=2.5, C3=10)

# ML
pipe = MLPipeline("rf").entrenar(X, y)
pred = pipe.predecir([100, 1])
```

## Licencia

MIT - kerbero05
