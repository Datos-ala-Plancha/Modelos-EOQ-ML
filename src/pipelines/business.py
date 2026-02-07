"""
Business Pipeline - Modelos EOQ para Gestión de Stock

Pipeline de negocio para optimización de inventarios.
"""

from dataclasses import dataclass
from typing import Dict, Tuple
import pandas as pd
import numpy as np


@dataclass
class EOQResult:
    """Resultado del cálculo EOQ"""

    Q_optimo: float
    costo_total: float
    costo_ordenamiento: float
    costo_mantenimiento: float
    numero_pedidos: float
    ciclo_dias: float
    punto_reorden: float = 0.0


class GestorStockPipeline:
    """Pipeline de gestión de stock con modelos EOQ"""

    @staticmethod
    def _validar(D: float, C1: float, C3: float) -> None:
        if D <= 0:
            raise ValueError("D debe ser positiva")
        if C1 <= 0:
            raise ValueError("C1 debe ser positivo")
        if C3 <= 0:
            raise ValueError("C3 debe ser positivo")

    @staticmethod
    def eoq_clasico(
        D: float,
        C1: float,
        C3: float,
        C4: float = 0,
        lead_time: float = 0,
        dias: int = 365,
    ) -> EOQResult:
        """EOQ Clásico: Q* = √(2DC₃/C₁)"""
        GestorStockPipeline._validar(D, C1, C3)

        Q = np.sqrt(2 * D * C3 / C1)
        costo_orden = (D / Q) * C3
        costo_mant = (Q / 2) * C1
        costo_compra = D * C4
        total = costo_compra + costo_orden + costo_mant

        return EOQResult(
            Q_optimo=Q,
            costo_total=total,
            costo_ordenamiento=costo_orden,
            costo_mantenimiento=costo_mant,
            numero_pedidos=D / Q,
            ciclo_dias=dias / (D / Q),
            punto_reorden=(D / dias) * lead_time,
        )

    @staticmethod
    def eoq_faltantes(
        D: float, C1: float, C2: float, C3: float, C4: float = 0, dias: int = 365
    ) -> Dict:
        """EOQ con Faltantes"""
        GestorStockPipeline._validar(D, C1, C3)
        if C2 <= 0:
            raise ValueError("C2 debe ser positivo")

        Q = np.sqrt(2 * D * C3 / C1) * np.sqrt((C1 + C2) / C2)
        S = Q * (C1 / (C1 + C2))
        Imax = Q - S

        costo_orden = (D / Q) * C3
        costo_mant = C1 * (Imax**2) / (2 * Q)
        costo_falt = C2 * (S**2) / (2 * Q)
        total = D * C4 + costo_orden + costo_mant + costo_falt

        return {
            "Q_optimo": Q,
            "S_max": S,
            "I_maximo": Imax,
            "costo_total": total,
            "costo_ordenamiento": costo_orden,
            "costo_mantenimiento": costo_mant,
            "costo_faltantes": costo_falt,
            "numero_pedidos": D / Q,
            "ciclo_dias": dias / (D / Q),
            "t1_dias": (Imax / D) * dias,
            "t2_dias": (S / D) * dias,
        }

    @staticmethod
    def eoq_descuentos(D: float, C3: float, i: float, rangos: list) -> Dict:
        """EOQ con Descuentos por Volumen"""
        mejor, menor = None, float("inf")

        for r in rangos:
            C1 = i * r["precio"]
            Q = np.sqrt(2 * D * C3 / C1)
            Q = (
                max(Q, r["min"])
                if Q < r["min"]
                else (r["max"] if "max" in r and Q > r["max"] else Q)
            )

            total = D * r["precio"] + (D / Q) * C3 + (Q / 2) * C1

            if total < menor:
                menor, mejor = (
                    total,
                    {
                        "Q_optimo": Q,
                        "precio_unitario": r["precio"],
                        "costo_total": total,
                        "costo_compra": D * r["precio"],
                        "costo_ordenamiento": (D / Q) * C3,
                        "costo_mantenimiento": (Q / 2) * C1,
                        "rango": r,
                    },
                )

        return mejor if mejor else {}

    @staticmethod
    def eoq_produccion(
        D: float,
        C1: float,
        C3: float,
        d: float = 0,
        p: float = 0,
        C4: float = 0,
        dias: int = 365,
    ) -> Dict:
        """EOQ de Producción"""
        GestorStockPipeline._validar(D, C1, C3)
        if p <= d:
            raise ValueError("p debe ser mayor que d")

        factor = 1 - (d / p) if d > 0 and p > 0 else 1
        Q = np.sqrt(2 * D * C3 / (C1 * factor))
        Imax = Q * factor

        return {
            "Q_optimo": Q,
            "I_maximo": Imax,
            "costo_total": D * C4 + (D / Q) * C3 + (Imax / 2) * C1,
            "costo_ordenamiento": (D / Q) * C3,
            "costo_mantenimiento": (Imax / 2) * C1,
            "numero_pedidos": D / Q,
            "ciclo_dias": dias / (D / Q),
            "tiempo_produccion_dias": (Q / p) * dias if p > 0 else 0,
            "factor_produccion": factor,
        }

    @staticmethod
    def abc(
        data: pd.DataFrame, col: str, umbral_a: float = 0.8, umbral_b: float = 0.95
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Clasificación ABC (Pareto)"""
        df = data.copy().sort_values(col, ascending=False)
        total = df[col].sum()
        df["pct_valor"] = (df[col] / total) * 100
        df["pct_acum"] = df["pct_valor"].cumsum()
        df["clase"] = df["pct_acum"].apply(
            lambda x: "A" if x <= umbral_a else ("B" if x <= umbral_b else "C")
        )

        stats = (
            df.groupby("clase")
            .agg({col: ["sum", "count"], "pct_valor": "sum"})
            .round(2)
        )
        stats.columns = ["_".join(c).strip() for c in stats.columns.values]

        return df, stats
