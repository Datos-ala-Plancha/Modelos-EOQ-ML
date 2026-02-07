import pytest
import pandas as pd
import numpy as np
from src.models.gestion_stock import GestorStock, EOQResult


class TestEOQClasico:
    def test_eoq_clasico_valores_basicos(self):
        D, C1, C3, C4 = 1000, 2.5, 10, 5
        resultado = GestorStock.eoq_clasico(D, C1, C3, C4)

        assert isinstance(resultado, EOQResult)
        assert resultado.Q_optimo > 0
        assert resultado.costo_total > 0
        assert resultado.numero_pedidos > 0

    def test_eoq_clasico_formula_correcta(self):
        D, C1, C3 = 1000, 2.5, 10
        Q_esperado = np.sqrt(2 * D * C3 / C1)
        resultado = GestorStock.eoq_clasico(D, C1, C3)

        assert np.isclose(resultado.Q_optimo, Q_esperado, rtol=1e-5)

    def test_eoq_clasico_con_lead_time(self):
        D, C1, C3, lead_time = 1000, 2.5, 10, 5
        resultado = GestorStock.eoq_clasico(D, C1, C3, lead_time=lead_time)

        assert resultado.punto_reorden > 0
        demanda_diaria = D / 365
        assert np.isclose(resultado.punto_reorden, demanda_diaria * lead_time)

    def test_eoq_clasico_error_demanda_cero(self):
        with pytest.raises(ValueError, match="La demanda.*positiva"):
            GestorStock.eoq_clasico(0, 2.5, 10)

    def test_eoq_clasico_error_costo_negativo(self):
        with pytest.raises(ValueError):
            GestorStock.eoq_clasico(1000, -1, 10)


class TestEOQConFaltantes:
    def test_eoq_faltantes_calculo(self):
        D, C1, C2, C3 = 450, 8750, 15000, 8000
        resultado = GestorStock.eoq_con_faltantes(D, C1, C2, C3)

        assert resultado["Q_optimo"] > 0
        assert resultado["S_max"] > 0
        assert resultado["I_maximo"] > 0
        assert resultado["costo_total"] > 0

    def test_eoq_faltantes_menor_q_mayor_faltantes(self):
        D, C1, C3 = 450, 8750, 8000
        resultado_alto = GestorStock.eoq_con_faltantes(D, C1, 50000, C3)
        resultado_bajo = GestorStock.eoq_con_faltantes(D, C1, 1000, C3)

        assert resultado_alto["S_max"] < resultado_bajo["S_max"]

    def test_eoq_faltantes_error_c2_cero(self):
        with pytest.raises(ValueError, match="costo de agotamiento.*positivo"):
            GestorStock.eoq_con_faltantes(450, 8750, 0, 8000)


class TestEOQConDescuentos:
    def test_eoq_descuentos_seleccion_optima(self):
        D, C3, i = 6000, 750, 0.1
        rangos = [
            {"min": 0, "max": 199, "precio": 4000},
            {"min": 200, "max": 499, "precio": 3500},
            {"min": 500, "max": 10000, "precio": 3000},
        ]
        resultado = GestorStock.eoq_con_descuentos(D, C3, i, rangos)

        assert resultado["Q_optimo"] > 0
        assert resultado["costo_total"] > 0
        assert "rango" in resultado

    def test_eoq_descuentos_rango_multiple(self):
        D, C3, i = 6000, 750, 0.1
        rangos = [
            {"min": 0, "max": 199, "precio": 4000},
            {"min": 200, "max": 499, "precio": 3500},
            {"min": 500, "max": 10000, "precio": 3000},
        ]
        resultado = GestorStock.eoq_con_descuentos(D, C3, i, rangos)

        assert resultado["Q_optimo"] >= rangos[0]["min"]


class TestEOQProduccion:
    def test_eoq_produccion_calculo(self):
        D, C1, C3 = 26000, 1.08, 135
        d, p = 26000 / 365, 60000 / 365
        resultado = GestorStock.eoq_produccion(D, C1, C3, d=d, p=p)

        assert resultado["Q_optimo"] > 0
        assert resultado["I_maximo"] > 0
        assert resultado["costo_total"] > 0

    def test_eoq_produccion_inventario_maximo(self):
        D, C1, C3 = 26000, 1.08, 135
        d, p = 26000 / 365, 60000 / 365
        resultado = GestorStock.eoq_produccion(D, C1, C3, d=d, p=p)

        factor = 1 - (d / p)
        Q = resultado["Q_optimo"]
        I_max_esperado = Q * factor

        assert np.isclose(resultado["I_maximo"], I_max_esperado, rtol=1e-5)

    def test_eoq_produccion_error_p_menor_d(self):
        D, C1, C3 = 26000, 1.08, 135
        with pytest.raises(ValueError, match="tasa de producción.*mayor"):
            GestorStock.eoq_produccion(D, C1, C3, d=100, p=50)


class TestClasificacionABC:
    def test_abc_clasificacion_basica(self):
        datos = pd.DataFrame(
            {
                "producto": ["A", "B", "C", "D", "E"],
                "valor": [1000, 500, 200, 100, 50],
            }
        )
        df_clasificado, estadisticas = GestorStock.clasificacion_stock_abc(
            datos, "valor", 0.8, 0.95
        )

        assert "clase_abc" in df_clasificado.columns
        assert "A" in df_clasificado["clase_abc"].values
        assert "B" in df_clasificado["clase_abc"].values
        assert "C" in df_clasificado["clase_abc"].values

    def test_abc_porcentajes_acumulados(self):
        datos = pd.DataFrame(
            {
                "producto": ["A", "B", "C"],
                "valor": [80, 15, 5],
            }
        )
        df_clasificado, _ = GestorStock.clasificacion_stock_abc(
            datos, "valor", 0.8, 0.95
        )

        assert df_clasificado.iloc[0]["porcentaje_acumulado"] <= 80
        assert df_clasificado.iloc[1]["porcentaje_acumulado"] <= 95

    def test_abc_ordena_descendente(self):
        datos = pd.DataFrame(
            {
                "producto": ["X", "Y", "Z"],
                "valor": [50, 100, 10],
            }
        )
        df_clasificado, _ = GestorStock.clasificacion_stock_abc(
            datos, "valor", 0.8, 0.95
        )

        assert df_clasificado.iloc[0]["valor"] == 100
        assert df_clasificado.iloc[1]["valor"] == 50
        assert df_clasificado.iloc[2]["valor"] == 10


class TestValidaciones:
    def test_validar_parametros_d_negativo(self):
        with pytest.raises(ValueError, match="La demanda.*positiva"):
            GestorStock.validar_parametros(-100, 2.5, 10)

    def test_validar_parametros_c1_cero(self):
        with pytest.raises(ValueError, match="costo de almacenamiento.*positivo"):
            GestorStock.validar_parametros(1000, 0, 10)

    def test_validar_parametros_c3_negativo(self):
        with pytest.raises(ValueError, match="costo de ordenamiento.*positivo"):
            GestorStock.validar_parametros(1000, 2.5, -10)
