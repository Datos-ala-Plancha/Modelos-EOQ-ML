"""
ML Pipeline - Modelos de Predicción de Demanda

Pipeline de Machine Learning para forecasting.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


@dataclass
class Metricas:
    mse: float
    rmse: float
    mae: float
    r2: float


class MLPipeline:
    """Pipeline de ML para predicción"""

    MODELOS = {
        "lineal": LinearRegression,
        "ridge": Ridge,
        "rf": RandomForestRegressor,
        "gb": GradientBoostingRegressor,
    }

    def __init__(self, modelo: str = "lineal", hiper: Optional[Dict] = None):
        if modelo not in self.MODELOS:
            raise ValueError(f"Modelo '{modelo}' no disponible")
        self.modelo = self.MODELOS[modelo](**(hiper or {}))
        self.entrenado = False
        self.features: Optional[List[str]] = None

    def entrenar(
        self, X: pd.DataFrame, y: pd.Series, test: float = 0.2, seed: int = 42
    ) -> Metricas:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test, random_state=seed
        )
        self.features = list(X.columns)
        self.modelo.fit(X_train, y_train)

        pred = self.modelo.predict(X_test)
        return Metricas(
            mse=mean_squared_error(y_test, pred),
            rmse=np.sqrt(mean_squared_error(y_test, pred)),
            mae=mean_absolute_error(y_test, pred),
            r2=r2_score(y_test, pred),
        )

    def predecir(self, vals: List[float]) -> float:
        if not self.entrenado:
            raise ValueError("No entrenado")
        return float(self.modelo.predict(np.array(vals).reshape(1, -1))[0])

    def importancia(self) -> Dict[str, float]:
        if not self.entrenado:
            raise ValueError("No entrenado")
        if hasattr(self.modelo, "feature_importances_"):
            imp = self.modelo.feature_importances_
        elif hasattr(self.modelo, "coef_"):
            imp = np.abs(self.modelo.coef_)
        else:
            raise ValueError("Sin importancia")
        return dict(zip(self.features, imp.tolist()))


class PredictorDemandaPipeline:
    """Pipeline de predicción de demanda"""

    @staticmethod
    def generar(
        n: int = 365,
        tendencia: float = 0.1,
        estacional: float = 10,
        ruido: float = 5,
        base: float = 100,
    ) -> pd.DataFrame:
        """Genera serie temporal sintética"""
        dias = np.arange(n)
        fechas = pd.date_range("2023-01-01", periods=n, freq="D")
        demanda = base + tendencia * dias + estacional * np.sin(2 * np.pi * dias / 365)
        demanda = np.maximum(demanda + np.random.normal(0, ruido, n), 0)
        return pd.DataFrame(
            {
                "fecha": fechas,
                "demanda": demanda,
                "dia": dias,
                "mes": fechas.month,
                "trimestre": fechas.quarter,
            }
        )

    @staticmethod
    def movils(serie: pd.Series, v: int = 7) -> pd.Series:
        """Promedio móvil"""
        return serie.rolling(v, min_periods=1).mean()

    @staticmethod
    def descomponer(
        serie: pd.Series, p: int = 365
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Descompone en tendencia, estacionalidad, residuo"""
        t = serie.rolling(p // 4, min_periods=1).mean()
        return (
            t,
            serie - t,
            serie - t - (serie - t),
        )
