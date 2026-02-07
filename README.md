# PYMESML

Proyecto de Machine Learning para análisis y predicción de datos de PYMES.

## Estructura

```
PYMESML/
├── data/           # Datos
│   ├── raw/        # Originales
│   └── processed/  # Transformados
├── notebooks/      # Jupyter notebooks
├── src/            # Código fuente
│   ├── data/       # Pipeline
│   ├── models/     # Modelos ML
│   └── utils/      # Utilidades
├── models/         # Modelos entrenados
├── app/            # Streamlit
├── docs/           # Documentación
└── tests/          # Tests
```

## Instalación

```bash
# Con conda
conda env create -f environment.yml
conda activate pymesml-env

# Con venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app/app.py
```
