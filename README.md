# PYMESML - Aplicación de Investigación Operativa

Aplicación web para gestión de inventarios y predicción de demanda, utilizando modelos EOQ (Economic Order Quantity) y Machine Learning.

## Características

### Gestión de Stock - Modelos EOQ
- **EOQ Clásico**: Cantidad económica de pedido tradicional
- **EOQ con Faltantes**: Modelo con backorders permitidos
- **EOQ con Descuentos**: Análisis de descuentos por volumen
- **EOQ de Producción**: Optimización para producción interna
- **Clasificación ABC**: Identificación de productos críticos

### Predicción de Demanda
- Generación de series temporales sintéticas
- Modelos de Machine Learning: Regresión Lineal, Ridge, Random Forest, Gradient Boosting
- Métricas de evaluación: R², RMSE, MAE, MSE

### Análisis de Datos
- Carga de datasets CSV
- Estadísticas descriptivas
- Visualizaciones: histogramas, boxplots, dispersión, series temporales
- Matriz de correlación

## Estructura del Proyecto

```
PYMESML/
├── app/                # Aplicación Streamlit
├── src/
│   └── models/         # Modelos y lógica de negocio
│       ├── gestion_stock.py
│       └── prediccion.py
├── tests/             # Pruebas unitarias
├── docs/              # Documentación
├── .streamlit/        # Configuración (tema oscuro)
├── requirements.txt   # Dependencias
└── README.md
```

## Instalación

```bash
# Clonar el repositorio
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

La aplicación se abrirá en http://localhost:8501

## Tecnologías

- **Streamlit**: Interfaz web interactiva
- **NumPy/Pandas**: Manipulación de datos
- **Scikit-learn**: Machine Learning
- **Plotly/Matplotlib**: Visualizaciones
- **EOQ Models**: Investigación Operativa

## Autor

Desarrollado para PYMES (Pequeñas y Medianas Empresas)

## Licencia

MIT
