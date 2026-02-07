import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.models.gestion_stock import GestorStock, EOQResult

st.set_page_config(page_title="PYMESML", page_icon="", layout="wide")

st.markdown(
    """
<div style="
    border: 2px solid #00FF41;
    border-radius: 15px;
    padding: 15px;
    margin: 5px 0;
">
<style>
    div.stMarkdown { margin-bottom: 5px; }
    p { margin-bottom: 5px; }
    .stMetric { padding: 2px 5px; margin: 2px; }
    div[data-testid='stExpander'] { margin-bottom: 5px; }
    hr { margin: 10px 0; }
</style>
<h1 style="margin: 5px 0 10px 0; font-size: 24px;">APLICACIÓN DE INVESTIGACIÓN OPERATIVA</h1>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Inicio", "Gestión de Stock", "Predicción", "Análisis", "Docs"]
)

with tab1:
    st.write("""
    ## Bienvenido a PYMESML

    - Analizar datos de PYMES
    - Realizar predicciones
    - Visualizar resultados
    - **Gestión de Stock con modelos EOQ**
    """)

with tab2:
    st.header("Sistema de Gestión de Stock - Modelos EOQ")
    st.markdown("### Investigación Operativa Aplicada a la Gestión de Inventarios")

    modelo = st.selectbox(
        "Seleccionar Modelo EOQ",
        [
            "EOQ Clásico",
            "EOQ con Faltantes",
            "EOQ con Descuentos",
            "EOQ de Producción",
            "Clasificación ABC",
        ],
    )

    if modelo == "EOQ Clásico":
        st.subheader("Modelo EOQ Clásico")
        st.caption("Cantidad Económica de Pedido para optimizar costos de inventario")

        col1, col2 = st.columns(2)

        with col1:
            D = st.number_input(
                "Demanda anual (unidades/año)",
                min_value=0.1,
                value=1000.0,
                step=10.0,
                help="Total de unidades demandadas por año. Puedes basarte en datos históricos de ventas.",
            )
            C1 = st.number_input(
                "Costo almacenamiento ($/unidad/año)",
                min_value=0.01,
                value=2.5,
                step=0.1,
                help="Costo de mantener una unidad en inventario durante un año. Incluye espacio, seguro, deterioro, etc.",
            )

        with col2:
            C3 = st.number_input(
                "Costo ordenamiento ($/pedido)",
                min_value=0.01,
                value=10.0,
                step=0.1,
                help="Costo fijo por cada pedido realizado. Incluye costos administrativos, transporte, etc.",
            )
            C4 = st.number_input(
                "Costo unitario compra ($/unidad)",
                min_value=0.0,
                value=5.0,
                step=0.1,
                help="Precio de compra por unidad del producto.",
            )

        lead_time = st.number_input(
            "Lead time (días)",
            min_value=0.0,
            value=5.0,
            step=1.0,
            help="Tiempo que tarda en llegar un pedido desde que se realiza hasta que se recibe.",
        )

        if st.button("Calcular EOQ Clásico"):
            try:
                resultado = GestorStock.eoq_clasico(D, C1, C3, C4, lead_time)

                st.success("Resultados del Cálculo EOQ")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Q* Óptimo",
                        f"{resultado.Q_optimo:.2f} unidades",
                        help="Cantidad óptima a pedir que minimiza el costo total de inventario.",
                    )
                    st.metric(
                        "Costo Total",
                        f"${resultado.costo_total:.2f}",
                        help="Costo anual total incluyendo compra, ordenamiento y mantenimiento.",
                    )

                with col2:
                    st.metric(
                        "Número de Pedidos",
                        f"{resultado.numero_pedidos:.2f}/año",
                        help="Veces al año que se realizará un pedido con la cantidad óptima.",
                    )
                    st.metric(
                        "Ciclo",
                        f"{resultado.ciclo_dias:.1f} días",
                        help="Días entre cada pedido.",
                    )

                with col3:
                    st.metric(
                        "Punto Reorden",
                        f"{resultado.punto_reorden:.1f} unidades",
                        help="Nivel de inventario en el que se debe realizar un nuevo pedido.",
                    )
                    st.metric(
                        "Costo Mantenimiento",
                        f"${resultado.costo_mantenimiento:.2f}",
                        help="Costo anual de mantener el inventario promedio.",
                    )

                with st.expander("Detalle de Costos"):
                    st.markdown(f"""
                    **Desglose de costos anuales:**
                    - Costo de Compra: ${D * C4:.2f}
                    - Costo de Ordenamiento: ${resultado.costo_ordenamiento:.2f}
                    - Costo de Mantenimiento: ${resultado.costo_mantenimiento:.2f}
                    """)

                st.info(
                    """
                **Interpretación:** Con Q* = {:.0f} unidades, harás {:.1f} pedidos al año 
                cada {:.1f} días. El punto de reorden de {:.0f} unidades te indica cuándo 
                realizar un nuevo pedido considerando el lead time de {:.0f} días.
                """.format(
                        resultado.Q_optimo,
                        resultado.numero_pedidos,
                        resultado.ciclo_dias,
                        resultado.punto_reorden,
                        lead_time,
                    )
                )

            except ValueError as e:
                st.error(f"Error: {e}")

    elif modelo == "EOQ con Faltantes":
        st.subheader("Modelo EOQ con Faltantes (Backorders)")
        st.caption("Permite agotamiento de stock con penalizaciones controladas")

        col1, col2 = st.columns(2)

        with col1:
            D = st.number_input(
                "Demanda anual (unidades/año)",
                min_value=0.1,
                value=450.0,
                step=10.0,
                help="Total de unidades demandadas por año.",
            )
            C1 = st.number_input(
                "Costo almacenamiento ($/unidad/año)",
                min_value=0.01,
                value=8750.0,
                step=100.0,
                help="Costo de mantener una unidad en inventario durante un año.",
            )

        with col2:
            C2 = st.number_input(
                "Costo faltante ($/unidad/año)",
                min_value=0.01,
                value=15000.0,
                step=100.0,
                help="Costo por cada unidad que no se puede satisfacer (penalización por falta de stock).",
            )
            C3 = st.number_input(
                "Costo ordenamiento ($/pedido)",
                min_value=0.01,
                value=8000.0,
                step=100.0,
                help="Costo fijo por cada pedido realizado.",
            )

        if st.button("Calcular EOQ con Faltantes"):
            try:
                resultado = GestorStock.eoq_con_faltantes(D, C1, C2, C3)

                st.success("Resultados del Cálculo EOQ con Faltantes")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Q* Óptimo",
                        f"{resultado['Q_optimo']:.1f} unidades",
                        help="Cantidad óptima a pedir considerando faltantes permitidos.",
                    )
                    st.metric(
                        "Faltantes Máximos (S)",
                        f"{resultado['S_max']:.1f} unidades",
                        help="Máximo nivel de faltantes esperado.",
                    )
                    st.metric(
                        "Inventario Máximo",
                        f"{resultado['I_maximo']:.1f} unidades",
                        help="Inventario máximo en bodega durante el ciclo.",
                    )

                with col2:
                    st.metric(
                        "Costo Total",
                        f"${resultado['costo_total']:.2f}",
                        help="Costo total anual incluyendo faltantes.",
                    )
                    st.metric(
                        "Número de Pedidos",
                        f"{resultado['numero_pedidos']:.1f}/año",
                        help="Pedidos por año con la cantidad óptima.",
                    )
                    st.metric(
                        "Ciclo",
                        f"{resultado['ciclo_dias']:.1f} días",
                        help="Días entre cada pedido.",
                    )

                with st.expander("Detalle de Costos"):
                    st.markdown(f"""
                    **Desglose de costos anuales:**
                    - Costo de Ordenamiento: ${resultado["costo_ordenamiento"]:.2f}
                    - Costo de Mantenimiento: ${resultado["costo_mantenimiento"]:.2f}
                    - Costo de Faltantes: ${resultado["costo_faltantes"]:.2f}
                    """)

                with st.expander("Análisis de Tiempos"):
                    st.markdown(f"""
                    **Tiempos del ciclo:**
                    - Tiempo con inventario positivo (t1): {resultado["t1_dias"]:.1f} días
                    - Tiempo con faltantes (t2): {resultado["t2_dias"]:.1f} días
                    """)

            except ValueError as e:
                st.error(f"Error: {e}")

    elif modelo == "EOQ con Descuentos":
        st.subheader("Modelo EOQ con Descuentos por Cantidad")
        st.caption("Análisis de descuentos por volumen de compra")

        col1, col2 = st.columns(2)

        with col1:
            D = st.number_input(
                "Demanda anual (unidades/año)", min_value=0.1, value=6000.0, step=100.0
            )
            C3 = st.number_input(
                "Costo ordenamiento ($/pedido)", min_value=0.01, value=750.0, step=10.0
            )

        with col2:
            i = st.number_input(
                "Tasa mantención (%)",
                min_value=0.01,
                max_value=1.0,
                value=0.1,
                step=0.01,
                format="%.2f",
            )

        st.markdown("### Rangos de Descuento")
        num_rangos = st.number_input(
            "Número de rangos", min_value=1, max_value=5, value=3
        )

        rangos = []
        for i in range(num_rangos):
            col1, col2, col3 = st.columns(3)
            with col1:
                min_qty = st.number_input(
                    f"Min rango {i + 1}",
                    min_value=0,
                    value=i * 200,
                    step=1,
                    key=f"min_{i}",
                )
            with col2:
                max_qty = st.number_input(
                    f"Max rango {i + 1}",
                    min_value=0,
                    value=(i + 1) * 200 - 1,
                    step=1,
                    key=f"max_{i}",
                )
            with col3:
                precio = st.number_input(
                    f"Precio rango {i + 1}",
                    min_value=0.01,
                    value=4000 - i * 500,
                    step=100,
                    key=f"precio_{i}",
                )

            rangos.append({"min": min_qty, "max": max_qty, "precio": precio})

        if st.button("Calcular EOQ con Descuentos"):
            try:
                resultado = GestorStock.eoq_con_descuentos(D, C3, i, rangos)

                st.success("Mejor Opción Encontrada")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Q* Óptimo", f"{resultado['Q_optimo']:.0f} unidades")
                    st.metric("Precio Unitario", f"${resultado['precio_unitario']:.2f}")

                with col2:
                    st.metric("Costo Total", f"${resultado['costo_total']:.2f}")
                    st.metric("Costo Compra", f"${resultado['costo_compra']:.2f}")

                with col3:
                    st.metric(
                        "Costo Ordenamiento", f"${resultado['costo_ordenamiento']:.2f}"
                    )
                    st.metric(
                        "Costo Mantenimiento",
                        f"${resultado['costo_mantenimiento']:.2f}",
                    )

                with st.expander("Rango Seleccionado"):
                    rango = resultado["rango"]
                    st.markdown(f"""
                    **Rango:** {rango["min"]} - {rango["max"] if "max" in rango else "∞"} unidades
                    **Precio por unidad:** ${rango["precio"]:.2f}
                    """)

            except ValueError as e:
                st.error(f"Error: {e}")

    elif modelo == "EOQ de Producción":
        st.subheader("Modelo EOQ de Producción")
        st.caption("Optimización para producción interna vs. compra externa")

        col1, col2 = st.columns(2)

        with col1:
            D = st.number_input(
                "Demanda anual (unidades/año)",
                min_value=0.1,
                value=26000.0,
                step=1000.0,
            )
            C1 = st.number_input(
                "Costo almacenamiento ($/unidad/año)",
                min_value=0.01,
                value=1.08,
                step=0.01,
            )

        with col2:
            C3 = st.number_input(
                "Costo preparación ($/lote)", min_value=0.01, value=135.0, step=1.0
            )
            d = st.number_input(
                "Tasa demanda (unidades/día)",
                min_value=0.0,
                value=26000 / 365,
                step=1.0,
            )
            p = st.number_input(
                "Tasa producción (unidades/día)",
                min_value=0.1,
                value=60000 / 365,
                step=1.0,
            )

        if st.button("Calcular EOQ de Producción"):
            try:
                resultado = GestorStock.eoq_produccion(D, C1, C3, d=d, p=p)

                st.success("Resultados del Cálculo EOQ de Producción")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Lote Óptimo Q*", f"{resultado['Q_optimo']:.0f} unidades")
                    st.metric(
                        "Inventario Máximo", f"{resultado['I_maximo']:.0f} unidades"
                    )
                    st.metric(
                        "Factor Producción", f"{resultado['factor_produccion']:.3f}"
                    )

                with col2:
                    st.metric("Costo Total", f"${resultado['costo_total']:.2f}")
                    st.metric(
                        "Número de Lotes", f"{resultado['numero_pedidos']:.1f}/año"
                    )
                    st.metric(
                        "Tiempo Producción",
                        f"{resultado['tiempo_produccion_dias']:.1f} días",
                    )

                with st.expander("Detalle de Costos"):
                    st.markdown(f"""
                    **Desglose de costos:**
                    - Costo de Preparación: ${resultado["costo_ordenamiento"]:.2f}
                    - Costo de Mantenimiento: ${resultado["costo_mantenimiento"]:.2f}
                    """)

            except ValueError as e:
                st.error(f"Error: {e}")

    elif modelo == "Clasificación ABC":
        st.subheader("Clasificación ABC de Inventario")
        st.caption("Identifica productos críticos según su valor de inversión")

        st.markdown("### Cargar Datos")
        uploaded_file = st.file_uploader(
            "Cargar archivo CSV con productos", type=["csv"]
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Vista previa:")
                st.dataframe(df.head())

                col1, col2 = st.columns(2)
                with col1:
                    columna_valor = st.selectbox(
                        "Columna de valor",
                        df.columns.tolist(),
                        help="Selecciona la columna que representa el valor o consumo.",
                    )
                with col2:
                    st.markdown("**Umbrales**")
                    umbral_a = st.slider(
                        "Umbral A (%)",
                        50,
                        95,
                        80,
                        help="Porcentaje acumulado para productos de alto valor.",
                    )
                    umbral_b = st.slider(
                        "Umbral B (%)",
                        75,
                        99,
                        95,
                    )

                if st.button("Ejecutar Clasificación"):
                    if columna_valor:
                        df_clasificado, estadisticas = (
                            GestorStock.clasificacion_stock_abc(
                                df, columna_valor, umbral_a / 100, umbral_b / 100
                            )
                        )
                        st.session_state["abc_data"] = df_clasificado
                        st.session_state["abc_stats"] = estadisticas
                        st.session_state["abc_umbrales"] = {
                            "a": umbral_a,
                            "b": umbral_b,
                        }
                        st.success("Clasificación completada")

            except Exception as e:
                st.error(f"Error: {e}")

        if "abc_data" in st.session_state:
            st.divider()
            st.markdown("### Resultados")

            res_tab1, res_tab2, res_tab3 = st.tabs(
                ["Tabla", "Distribución", "Curva ABC"]
            )

            with res_tab1:
                st.dataframe(st.session_state["abc_data"])

            with res_tab2:
                col1, col2 = st.columns(2)
                with col1:
                    fig_pie = px.pie(
                        st.session_state["abc_data"],
                        names="clase_abc",
                        title="Distribución por Clase",
                        color="clase_abc",
                        color_discrete_map={
                            "A": "#e63946",
                            "B": "#f4a261",
                            "C": "#2a9d8f",
                        },
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                with col2:
                    st.dataframe(st.session_state["abc_stats"])

            with res_tab3:
                umbrales = st.session_state.get("abc_umbrales", {"a": 80, "b": 95})
                fig_line = px.line(
                    st.session_state["abc_data"].sort_values("porcentaje_acumulado"),
                    x=np.arange(len(st.session_state["abc_data"])),
                    y="porcentaje_acumulado",
                    title="Curva ABC",
                    labels={
                        "x": "Productos (ordenados)",
                        "porcentaje_acumulado": "% Valor Acumulado",
                    },
                )
                fig_line.add_hline(
                    y=umbrales["a"],
                    line_dash="dash",
                    line_color="#e63946",
                    annotation_text=f"{umbrales['a']}%",
                )
                fig_line.add_hline(
                    y=umbrales["b"],
                    line_dash="dash",
                    line_color="#f4a261",
                    annotation_text=f"{umbrales['b']}%",
                )
                st.plotly_chart(fig_line, use_container_width=True)

with tab3:
    from src.models.prediccion import PredictorDemanda, SimuladorDemanda

    st.header("Predicción de Demanda")
    st.markdown("Modelos de Machine Learning para forecasting")

    pred_tab1, pred_tab2, pred_tab3 = st.tabs(
        ["Generar Datos", "Entrenar Modelo", "Predecir"]
    )

    with pred_tab1:
        st.subheader("Generar Datos de Demanda Sintéticos")
        col1, col2, col3 = st.columns(3)
        with col1:
            n_dias = st.number_input("Días", 30, 3650, 365)
        with col2:
            tendencia = st.number_input("Tendencia", -10.0, 10.0, 0.5, 0.1)
        with col3:
            estacionalidad = st.number_input("Estacionalidad", 0.0, 100.0, 15.0, 1.0)

        if st.button("Generar Serie Temporal"):
            df_demanda = SimuladorDemanda.generar_demanda_historica(
                n_periodos=int(n_dias),
                tendencia=float(tendencia),
                estacionalidad=float(estacionalidad),
            )
            st.session_state["df_demanda"] = df_demanda
            st.success("Serie temporal generada")

    with pred_tab2:
        st.subheader("Entrenar Modelo Predictivo")
        if "df_demanda" in st.session_state:
            df = st.session_state["df_demanda"]

            st.write("Vista previa de datos:")
            st.dataframe(df.head())

            modelo_seleccionado = st.selectbox(
                "Seleccionar Modelo",
                ["regresion_lineal", "ridge", "random_forest", "gradient_boosting"],
            )

            columnas_features = st.multiselect(
                "Características",
                ["dia", "mes", "trimestre"],
                default=["dia", "mes"],
            )

            columna_objetivo = st.selectbox("Objetivo", ["demanda"])

            if st.button("Entrenar Modelo"):
                if not columnas_features:
                    st.error("Selecciona al menos una característica")
                else:
                    X = df[columnas_features]
                    y = df[columna_objetivo]

                    predictor = PredictorDemanda(modelo=modelo_seleccionado)
                    metricas = predictor.entrenar(X, y)

                    st.session_state["predictor"] = predictor

                    st.success("Modelo entrenado")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("R²", f"{metricas.r2:.4f}")
                    with col2:
                        st.metric("RMSE", f"{metricas.rmse:.2f}")
                    with col3:
                        st.metric("MAE", f"{metricas.mae:.2f}")
                    with col4:
                        st.metric("MSE", f"{metricas.mse:.2f}")

                    if hasattr(predictor, "importancia_caracteristicas"):
                        importancia = predictor.importancia_caracteristicas()
                        st.markdown("**Importancia de Características:**")
                        importancia_df = pd.DataFrame(
                            list(importancia.items()),
                            columns=["Característica", "Importancia"],
                        ).sort_values("Importancia", ascending=False)
                        st.dataframe(importancia_df)
        else:
            st.info("Genera datos primero en la pestaña 'Generar Datos'")

    with pred_tab3:
        st.subheader("Realizar Predicciones")
        if "predictor" in st.session_state:
            predictor = st.session_state["predictor"]

            st.markdown("**Características del modelo:**")
            if predictor.feature_names:
                st.write(", ".join(predictor.feature_names))

            st.markdown("### Ingresar valores para predicción")
            valores = []
            cols = st.columns(len(predictor.feature_names))

            for i, feature in enumerate(predictor.feature_names):
                with cols[i]:
                    val = st.number_input(f"{feature}", value=100.0)
                    valores.append(val)

            if st.button("Predecir"):
                try:
                    prediccion = predictor.predecir_valores(valores)
                    st.success(f"**Demanda Predicha:** {prediccion:.2f} unidades")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("Entrena un modelo primero")

with tab4:
    st.header("Análisis de Datos")
    st.markdown("Visualizaciones y análisis exploratorio")

    anal_tab1, anal_tab2, anal_tab3, anal_tab4 = st.tabs(
        ["Cargar Datos", "Estadísticas", "Visualizaciones", "Correlación"]
    )

    with anal_tab1:
        st.subheader("Cargar Dataset")
        archivo = st.file_uploader("Subir CSV", type=["csv"])

        if archivo is not None:
            df = pd.read_csv(archivo)
            st.session_state["df_analisis"] = df
            st.success("Datos cargados")
            st.dataframe(df.head())
            st.write(f"**Filas:** {df.shape[0]}, **Columnas:** {df.shape[1]}")

    with anal_tab2:
        st.subheader("Estadísticas Descriptivas")
        if "df_analisis" in st.session_state:
            df = st.session_state["df_analisis"]
            columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

            if columnas_numericas:
                st.write("**Resumen estadístico:**")
                st.dataframe(df[columnas_numericas].describe().T)

                st.write("**Valores nulos:**")
                nulos = df.isnull().sum()
                st.dataframe(nulos[nulos > 0])
            else:
                st.warning("No hay columnas numéricas")
        else:
            st.info("Carga datos primero")

    with anal_tab3:
        st.subheader("Visualizaciones")
        if "df_analisis" in st.session_state:
            df = st.session_state["df_analisis"]
            columnas = df.columns.tolist()

            tipo_grafico = st.selectbox(
                "Tipo de gráfico",
                ["Histograma", "Boxplot", "Dispersión", "Línea temporal"],
            )

            if tipo_grafico in ["Histograma", "Boxplot"]:
                columna = st.selectbox("Columna", columnas)
                if st.button("Generar"):
                    fig, ax = plt.subplots(figsize=(10, 5))
                    if tipo_grafico == "Histograma":
                        ax.hist(
                            df[columna].dropna(), bins=30, edgecolor="black", alpha=0.7
                        )
                    else:
                        ax.boxplot(df[columna].dropna())
                    ax.set_title(f"{tipo_grafico}: {columna}")
                    st.pyplot(fig)

            elif tipo_grafico == "Dispersión":
                col_x, col_y = st.columns(2)
                with col_x:
                    x = st.selectbox("Eje X", columnas)
                with col_y:
                    y = st.selectbox("Eje Y", columnas)
                if st.button("Generar"):
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.scatter(df[x], df[y], alpha=0.5)
                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title(f"Dispersión: {x} vs {y}")
                    st.pyplot(fig)

            elif tipo_grafico == "Línea temporal":
                columnas_tiempo = [
                    c for c in columnas if "fecha" in c.lower() or "date" in c.lower()
                ]
                if columnas_tiempo:
                    fecha_col = st.selectbox("Columna fecha", columnas_tiempo)
                    valor_col = st.selectbox("Columna valor", columnas)
                    if st.button("Generar"):
                        df[fecha_col] = pd.to_datetime(df[fecha_col])
                        df_sorted = df.sort_values(fecha_col)
                        fig, ax = plt.subplots(figsize=(12, 5))
                        ax.plot(df_sorted[fecha_col], df_sorted[valor_col])
                        ax.set_xlabel(fecha_col)
                        ax.set_ylabel(valor_col)
                        ax.set_title("Serie temporal")
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                else:
                    st.warning("No se encontró columna de fecha")
        else:
            st.info("Carga datos primero")

    with anal_tab4:
        st.subheader("Matriz de Correlación")
        st.caption("Identifica relaciones entre variables numéricas")
        if "df_analisis" in st.session_state:
            df = st.session_state["df_analisis"]
            numericas = df.select_dtypes(include=[np.number]).columns.tolist()

            if len(numericas) > 1:
                corr = df[numericas].corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
                ax.set_xticks(range(len(numericas)))
                ax.set_yticks(range(len(numericas)))
                ax.set_xticklabels(numericas, rotation=45, ha="right", fontsize=10)
                ax.set_yticklabels(numericas, fontsize=10)
                ax.set_title("Matriz de Correlación", fontsize=12)

                for i in range(len(numericas)):
                    for j in range(len(numericas)):
                        text = ax.text(
                            j,
                            i,
                            f"{corr.iloc[i, j]:.2f}",
                            ha="center",
                            va="center",
                            color="black",
                            fontsize=9,
                        )

                plt.colorbar(im, ax=ax, label="Correlación")
                st.pyplot(fig)

                st.write("**Valores de correlación:**")
                st.dataframe(corr.round(2))
            else:
                st.warning("Se necesitan al least 2 columnas numéricas")
        else:
            st.info("Carga datos primero")

with tab5:
    st.header("Documentación")
    st.markdown("""
    ## Sistema de Gestión de Stock

    ### Modelos EOQ Implementados:

    1. **EOQ Clásico**: Cantidad Económica de Pedido tradicional
    2. **EOQ con Faltantes**: Permite backorders con costos de penalización
    3. **EOQ con Descuentos**: Análisis de descuentos por volumen
    4. **EOQ de Producción**: Optimización para producción interna
    5. **Clasificación ABC**: Identificación de productos críticos

    ### Fórmulas Clave:

    - **EOQ Clásico**: Q* = √(2DC₃/C₁)
    - **EOQ con Faltantes**: Q* = √(2DC₃/C₁) × √((C₁+C₂)/C₂)
    - **EOQ Producción**: Q* = √(2DC₃/[C₁(1-d/p)])

    Donde:
    - D = Demanda anual
    - C₁ = Costo de almacenamiento
    - C₂ = Costo de faltantes
    - C₃ = Costo de ordenamiento/preparación
    - d = Tasa de demanda
    - p = Tasa de producción
    """)

st.markdown("---")
st.markdown("*PYMESML v1.0.0 - Gestión de Stock con Modelos EOQ*")

st.markdown("</div>", unsafe_allow_html=True)
