"""
PYMESML - Aplicación de Investigación Operativa

MVP con estructura de pipelines modulares.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(__file__))
from src.pipelines.business import GestorStockPipeline
from src.pipelines.ml import MLPipeline, PredictorDemandaPipeline

st.set_page_config(page_title="PYMESML", layout="wide")

st.markdown(
    """
<div style="border: 2px solid #00FF41; border-radius: 15px; padding: 15px;">
<style>
    p { margin-bottom: 5px; }
    .stMetric { padding: 2px 5px; margin: 2px; }
    hr { margin: 10px 0; }
</style>
<h1 style="margin: 5px 0 10px 0; font-size: 24px;">APLICACIÓN DE INVESTIGACIÓN OPERATIVA</h1>
""",
    unsafe_allow_html=True,
)

tabs = st.tabs(["Inicio", "Gestión Stock", "Predicción", "Análisis", "Docs"])

# === INICIO ===
with tabs[0]:
    st.write("""
    ## Bienvenido a PYMESML
    - Análisis de datos para PYMES
    - Predicción de demanda con ML
    - Modelos EOQ para inventarios
    """)

# === GESTIÓN DE STOCK ===
with tabs[1]:
    st.header("Gestión de Stock - Modelos EOQ")
    modelo = st.selectbox(
        "Modelo",
        ["EOQ Clásico", "EOQ Faltantes", "EOQ Descuentos", "EOQ Producción", "ABC"],
    )

    if modelo == "EOQ Clásico":
        c1, c2 = st.columns(2)
        with c1:
            D = st.number_input("Demanda anual", 0.1, 1000000.0, 1000.0, 10.0)
            C1 = st.number_input("Costo almacenamiento ($)", 0.01, 10000.0, 2.5, 0.1)
        with c2:
            C3 = st.number_input("Costo ordenamiento ($)", 0.01, 10000.0, 10.0, 0.1)
            C4 = st.number_input("Costo unitario ($)", 0.0, 1000.0, 5.0, 0.1)
        lead = st.number_input("Lead time (días)", 0.0, 365.0, 5.0, 1.0)

        if st.button("Calcular"):
            r = GestorStockPipeline.eoq_clasico(D, C1, C3, C4, lead)
            st.success("Resultados EOQ Clásico")
            m1, m2, m3 = st.columns(3)
            m1.metric("Q* Óptimo", f"{r.Q_optimo:.1f} unidades")
            m2.metric("Costo Total", f"${r.costo_total:.2f}")
            m3.metric("Pedidos/Año", f"{r.numero_pedidos:.1f}")
            m1.metric("Ciclo", f"{r.ciclo_dias:.1f} días")
            m2.metric("Punto Reorden", f"{r.punto_reorden:.1f}")
            m3.metric("Costo Mantenimiento", f"${r.costo_mantenimiento:.2f}")

    elif modelo == "EOQ Faltantes":
        c1, c2 = st.columns(2)
        with c1:
            D = st.number_input("Demanda", 0.1, 100000.0, 450.0, 10.0)
            C1 = st.number_input("C1", 0.01, 100000.0, 8750.0, 100.0)
        with c2:
            C2 = st.number_input("Costo faltante", 0.01, 100000.0, 15000.0, 100.0)
            C3 = st.number_input("C3", 0.01, 100000.0, 8000.0, 100.0)

        if st.button("Calcular"):
            r = GestorStockPipeline.eoq_faltantes(D, C1, C2, C3)
            st.success("Resultados")
            m1, m2 = st.columns(2)
            m1.metric("Q*", f"{r['Q_optimo']:.1f}")
            m2.metric("Costo Total", f"${r['costo_total']:.2f}")
            m1.metric("Faltantes Máx", f"{r['S_max']:.1f}")
            m2.metric("Inventario Máx", f"{r['I_maximo']:.1f}")

    elif modelo == "EOQ Descuentos":
        c1, c2 = st.columns(2)
        with c1:
            D = st.number_input("Demanda", 0.1, 100000.0, 6000.0, 100.0)
            C3 = st.number_input("C3", 0.01, 10000.0, 750.0, 10.0)
        with c2:
            i = st.number_input("Tasa mantención", 0.01, 1.0, 0.1, 0.01, format="%.2f")

        n = st.number_input("Rangos", 1, 5, 3)
        rangos = []
        for r in range(n):
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                mn = st.number_input(f"Min {r + 1}", 0, 1000000, r * 200, 1)
            with rc2:
                mx = st.number_input(f"Max {r + 1}", 0, 1000000, (r + 1) * 200 - 1, 1)
            with rc3:
                pr = st.number_input(
                    f"Precio {r + 1}", 0.01, 100000.0, 4000 - r * 500, 100.0
                )
            rangos.append({"min": mn, "max": mx, "precio": pr})

        if st.button("Calcular"):
            r = GestorStockPipeline.eoq_descuentos(D, C3, i, rangos)
            st.success(f"Mejor: Q={r['Q_optimo']:.0f}, ${r['costo_total']:.2f}")
            st.write(f"Precio: ${r['precio_unitario']:.2f}")

    elif modelo == "EOQ Producción":
        c1, c2 = st.columns(2)
        with c1:
            D = st.number_input("Demanda", 0.1, 1000000.0, 26000.0, 1000.0)
            C1 = st.number_input("C1", 0.01, 100.0, 1.08, 0.01)
        with c2:
            C3 = st.number_input("C3", 0.01, 10000.0, 135.0, 1.0)
            d = st.number_input("Tasa demanda", 0.0, 10000.0, 26000 / 365, 1.0)
            p = st.number_input("Tasa producción", 0.1, 100000.0, 60000 / 365, 1.0)

        if st.button("Calcular"):
            r = GestorStockPipeline.eoq_produccion(D, C1, C3, d, p)
            st.success("Resultados")
            m1, m2 = st.columns(2)
            m1.metric("Q*", f"{r['Q_optimo']:.0f}")
            m2.metric("Costo Total", f"${r['costo_total']:.2f}")
            m1.metric("Inventario Máx", f"{r['I_maximo']:.0f}")
            m2.metric("Tiempo Prod", f"{r['tiempo_produccion_dias']:.1f} días")

    elif modelo == "ABC":
        file = st.file_uploader("CSV productos", type=["csv"])
        if file:
            df = pd.read_csv(file)
            col = st.selectbox("Columna valor", df.columns)
            a = st.slider("Umbral A (%)", 50, 95, 80) / 100
            b = st.slider("Umbral B (%)", 75, 99, 95) / 100
            if st.button("Clasificar"):
                res, stats = GestorStockPipeline.abc(df, col, a, b)
                st.session_state["abc"] = res
                st.session_state["abc_stats"] = stats
                st.success("Completado")

        if "abc" in st.session_state:
            tabA, tabB, tabC = st.tabs(["Tabla", "Distribución", "Curva"])
            with tabA:
                st.dataframe(st.session_state["abc"])
            with tabB:
                fig = px.pie(
                    st.session_state["abc"],
                    names="clase",
                    title="ABC",
                    color="clase",
                    color_discrete_map={"A": "#e63946", "B": "#f4a261", "C": "#2a9d8f"},
                )
                st.plotly_chart(fig)
            with tabC:
                fig = px.line(
                    st.session_state["abc"].sort_values("pct_acum"),
                    x=np.arange(len(st.session_state["abc"])),
                    y="pct_acum",
                    title="Curva ABC",
                )
                fig.add_hline(y=a * 100, line_dash="dash", line_color="#e63946")
                st.plotly_chart(fig)

# === PREDICCIÓN ===
with tabs[2]:
    st.header("Predicción de Demanda")
    ptabs = st.tabs(["Generar", "Entrenar", "Predecir"])

    with ptabs[0]:
        c1, c2, c3 = st.columns(3)
        n = c1.number_input("Días", 30, 3650, 365)
        t = c2.number_input("Tendencia", -10.0, 10.0, 0.5, 0.1)
        e = c3.number_input("Estacionalidad", 0.0, 100.0, 15.0, 1.0)
        if st.button("Generar"):
            st.session_state["df_dem"] = PredictorDemandaPipeline.generar(n, t, e)
            st.success("Generado")

    with ptabs[1]:
        if "df_dem" in st.session_state:
            st.dataframe(st.session_state["df_dem"].head())
            m = st.selectbox("Modelo", ["lineal", "ridge", "rf", "gb"])
            feats = st.multiselect(
                "Features", ["dia", "mes", "trimestre"], default=["dia", "mes"]
            )
            if st.button("Entrenar"):
                X = st.session_state["df_dem"][feats]
                y = st.session_state["df_dem"]["demanda"]
                pipe = MLPipeline(m).entrenar(X, y)
                st.session_state["pipe"] = pipe
                imp = pipe.importancia()
                st.success(f"R²: {imp.pop('r2', 0):.4f}")
                st.dataframe(
                    pd.DataFrame(
                        imp.items(), columns=["Feature", "Importancia"]
                    ).sort_values("Importancia", ascending=False)
                )
        else:
            st.info("Genera datos primero")

    with ptabs[2]:
        if "pipe" in st.session_state:
            p = st.session_state["pipe"]
            vals = [st.number_input(f, 0.0, 10000.0, 100.0) for f in p.features]
            if st.button("Predecir"):
                r = p.predecir(vals)
                st.success(f"Demanda: {r:.2f}")
        else:
            st.info("Entrena modelo primero")

# === ANÁLISIS ===
with tabs[3]:
    st.header("Análisis de Datos")
    atabs = st.tabs(["Cargar", "Estadísticas", "Gráficos", "Correlación"])

    with atabs[0]:
        f = st.file_uploader("CSV", type=["csv"])
        if f:
            st.session_state["df_anal"] = pd.read_csv(f)
            st.dataframe(st.session_state["df_anal"].head())

    with atabs[1]:
        if "df_anal" in st.session_state:
            nums = (
                st.session_state["df_anal"].select_dtypes(include=[np.number]).columns
            )
            st.dataframe(st.session_state["df_anal"][nums].describe().T)

    with atabs[2]:
        if "df_anal" in st.session_state:
            tipo = st.selectbox("Tipo", ["Histograma", "Boxplot", "Dispersión"])
            col = st.selectbox("Columna", st.session_state["df_anal"].columns)
            if st.button("Generar"):
                fig, ax = plt.subplots(figsize=(8, 4))
                if tipo == "Histograma":
                    ax.hist(
                        st.session_state["df_anal"][col].dropna(),
                        bins=30,
                        edgecolor="black",
                    )
                else:
                    ax.boxplot(st.session_state["df_anal"][col].dropna())
                ax.set_title(f"{tipo}: {col}")
                st.pyplot(fig)

    with atabs[3]:
        if "df_anal" in st.session_state:
            nums = (
                st.session_state["df_anal"].select_dtypes(include=[np.number]).columns
            )
            if len(nums) > 1:
                corr = st.session_state["df_anal"][nums].corr()
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
                ax.set_xticks(range(len(nums)))
                ax.set_yticks(range(len(nums)))
                ax.set_xticklabels(nums, rotation=45)
                ax.set_yticklabels(nums)
                for i in range(len(nums)):
                    for j in range(len(nums)):
                        ax.text(
                            j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center"
                        )
                st.pyplot(fig)
                st.dataframe(corr.round(2))

# === DOCS ===
with tabs[4]:
    st.header("Documentación")
    st.markdown("""
    ## Modelos EOQ
    - **Clásico**: Q* = √(2DC₃/C₁)
    - **Faltantes**: Con backorders
    - **Descuentos**: Por volumen
    - **Producción**: Tasa finita
    - **ABC**: Clasificación Pareto

    ## ML
    - Lineal, Ridge, Random Forest, Gradient Boosting
    """)

st.markdown("---")
st.markdown("*PYMESML v1.0.0 - MIT License*")
st.markdown("</div>", unsafe_allow_html=True)
