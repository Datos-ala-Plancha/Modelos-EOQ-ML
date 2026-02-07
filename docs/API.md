# Documentación de la API

## Módulos Principales

### src.models.gestion_stock

#### EOQResult
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

#### GestorStock

##### eoq_clasico()
```python
def eoq_clasico(
    D: float,
    C1: float,
    C3: float,
    C4: float = 0,
    lead_time_dias: float = 0,
    dias_anio: int = 365,
) -> EOQResult
```
Calcula la cantidad económica de pedido clásica.

##### eoq_con_faltantes()
```python
def eoq_con_faltantes(
    D: float, C1: float, C2: float, C3: float, C4: float = 0, dias_anio: int = 365
) -> Dict
```
Modelo EOQ con backorders permitidos.

##### eoq_con_descuentos()
```python
def eoq_con_descuentos(D: float, C3: float, i: float, rangos_precio: list) -> Dict
```
Análisis de descuentos por volumen.

##### eoq_produccion()
```python
def eoq_produccion(
    D: float, C1: float, C3: float, C4: float = 0, d: float = 0, p: float = 0, dias_anio: int = 365
) -> Dict
```
Modelo EOQ para producción interna.

##### clasificacion_stock_abc()
```python
def clasificacion_stock_abc(
    data: pd.DataFrame,
    valor_columna: str,
    umbral_a: float = 0.8,
    umbral_b: float = 0.95,
) -> Tuple[pd.DataFrame, pd.DataFrame]
```
Clasificación ABC de inventarios.

---

## src.models.prediccion

### PredictorDemanda
```python
class PredictorDemanda:
    MODELOS_DISPONIBLES = {
        "regresion_lineal": LinearRegression,
        "ridge": Ridge,
        "random_forest": RandomForestRegressor,
        "gradient_boosting": GradientBoostingRegressor,
    }

    def entrenar(X: pd.DataFrame, y: pd.Series) -> MetricasModelo
    def predecir(X: pd.DataFrame) -> np.ndarray
    def importancia_caracteristicas() -> Dict[str, float]
```

### SimuladorDemanda
```python
class SimuladorDemanda:
    @staticmethod
    def generar_demanda_historica(...) -> pd.DataFrame
    @staticmethod
    def tendencia_promedio_movil(demanda: pd.Series, ventana: int = 7) -> pd.Series
```
