"""
EDA Agent - Agente de Análisis Exploratorio de Datos

Agente conversacional para análisis de datos.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from scipy import stats


class EDAAgent:
    """Agente conversacional para EDA"""

    def __init__(self):
        self.df = None
        self.df_info = {}

    def saludar(self):
        print("""
╔═══════════════════════════════════════════════════════════╗
║         EDA Agent - Tu Asistente de Análisis           ║
╠═══════════════════════════════════════════════════════════╣
║  Puedo ayudarte con:                                 ║
║  • Carga de datasets (CSV, Excel, JSON)               ║
║  • Análisis estadístico descriptivo                    ║
║  • Detección de valores atípicos                     ║
║  • Visualizaciones automáticas                         ║
║  • Correlación entre variables                       ║
║  • Detección de valores faltantes                    ║
╚═══════════════════════════════════════════════════════════╝
        """)

    def mostrar_ayuda(self):
        print("""
📋 Comandos disponibles:
  /cargar       → Cargar dataset
  /info         → Información del dataset
  /head         → Primeras filas
  /tail         → Últimas filas
  /shape        → Dimensiones
  /dtypes       → Tipos de datos
  /describe     → Estadísticas descriptivas
  /nulos        → Valores faltantes
  /correlacion  → Matriz de correlación
  /outliers     → Detectar valores atípicos
  /hist         → Histograma de variable
  /boxplot      → Boxplot de variable
  /scatter       → Gráfico de dispersión
  /categorico    → Análisis de variables categóricas
  /resumen      → Resumen completo del EDA
  /ayuda        → Mostrar ayuda
  /salir        → Terminar
        """)

    def cargar_dataset(self):
        print("\n📂 Cargar Dataset")
        print("  Formatos: CSV, Excel (.xlsx), JSON")
        ruta = input("  Ruta del archivo: ").strip()

        if not os.path.exists(ruta):
            print(f"❌ Archivo no encontrado: {ruta}")
            return

        try:
            if ruta.endswith(".csv"):
                self.df = pd.read_csv(ruta)
            elif ruta.endswith(".xlsx"):
                self.df = pd.read_excel(ruta)
            elif ruta.endswith(".json"):
                self.df = pd.read_json(ruta)
            else:
                print("❌ Formato no soportado")
                return

            print(
                f"\n✅ Dataset cargado: {self.df.shape[0]} filas × {self.df.shape[1]} columnas"
            )
            self._analizar_dataset()
        except Exception as e:
            print(f"❌ Error: {e}")

    def _analizar_dataset(self):
        """Analiza el dataset al cargarlo"""
        if self.df is None:
            return

        self.df_info = {
            "nulos": self.df.isnull().sum(),
            "tipos": self.df.dtypes,
            "numericas": self.df.select_dtypes(include=[np.number]).columns.tolist(),
            "categoricas": self.df.select_dtypes(include=["object"]).columns.tolist(),
        }

    def mostrar_info(self):
        print("\n📊 Información del Dataset")
        if self.df is None:
            print("❌ No hay dataset cargado. Usa /cargar")
            return

        print(f"""
┌─────────────────── Info ───────────────────┐
│ Filas:         {self.df.shape[0]:>10}                    │
│ Columnas:       {self.df.shape[1]:>10}                    │
│ Memoria:        {self.df.memory_usage(deep=True).sum() / 1024:.1f} KB                   │
└─────────────────────────────────────────────┘
        """)

    def mostrar_head(self):
        if self.df is None:
            print("❌ No hay dataset")
            return
        n = int(input("  Filas a mostrar (default 5): ") or 5)
        print(f"\n📋 Primeras {n} filas:")
        print(self.df.head(n).to_string())

    def mostrar_tail(self):
        if self.df is None:
            print("❌ No hay dataset")
            return
        n = int(input("  Filas a mostrar (default 5): ") or 5)
        print(f"\n📋 Últimas {n} filas:")
        print(self.df.tail(n).to_string())

    def mostrar_shape(self):
        if self.df is None:
            print("❌ No hay dataset")
            return
        print(
            f"\n📐 Dimensiones: {self.df.shape[0]} filas × {self.df.shape[1]} columnas"
        )

    def mostrar_dtypes(self):
        if self.df is None:
            print("❌ No hay dataset")
            return
        print("\n📝 Tipos de datos:")
        print(self.df.dtypes.to_string())

    def mostrar_describe(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        print("\n📈 Estadísticas Descriptivas")
        cols = self.df_info.get(
            "numericas", self.df.select_dtypes(include=[np.number]).columns.tolist()
        )

        if not cols:
            print("  No hay columnas numéricas")
            return

        print("\nVariables numéricas:")
        for col in cols[:5]:  # Mostrar máximo 5
            print(f"\n  {col}:")
            s = self.df[col].describe()
            print(f"    Count: {s['count']:.0f}")
            print(f"    Mean:  {s['mean']:.2f}")
            print(f"    Std:   {s['std']:.2f}")
            print(f"    Min:   {s['min']:.2f}")
            print(f"    25%:   {s['25%']:.2f}")
            print(f"    50%:   {s['50%']:.2f}")
            print(f"    75%:   {s['75%']:.2f}")
            print(f"    Max:   {s['max']:.2f}")

    def mostrar_nulos(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        print("\n🔍 Valores Faltantes")
        nulos = self.df.isnull().sum()
        total_nulos = nulos.sum()

        if total_nulos == 0:
            print("  ✅ No hay valores faltantes")
            return

        print(f"  Total valores faltantes: {total_nulos}")
        print("\n  Por columna:")
        for col in nulos[nulos > 0].index:
            pct = (nulos[col] / len(self.df)) * 100
            print(f"    {col}: {nulos[col]} ({pct:.1f}%)")

    def mostrar_correlacion(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        numericas = self.df_info.get(
            "numericas", self.df.select_dtypes(include=[np.number]).columns.tolist()
        )

        if len(numericas) < 2:
            print("  Se necesitan al menos 2 variables numéricas")
            return

        print("\n🔗 Matriz de Correlación")
        corr = self.df[numericas].corr()

        print("\n  Variables más correlacionadas:")
        # Encontrar pares más correlacionados
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                val = corr.iloc[i, j]
                if abs(val) > 0.7:
                    print(f"    {corr.columns[i]} ↔ {corr.columns[j]}: {val:.3f}")

        print("\n  Matriz completa:")
        print(corr.round(2).to_string())

    def detectar_outliers(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        numericas = self.df_info.get(
            "numericas", self.df.select_dtypes(include=[np.number]).columns.tolist()
        )

        print("\n🔎 Detección de Outliers (IQR Method)")

        for col in numericas:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outliers = self.df[(self.df[col] < lower) | (self.df[col] > upper)][col]
            n_outliers = len(outliers)

            if n_outliers > 0:
                print(f"\n  {col}:")
                print(f"    Rango válido: [{lower:.2f}, {upper:.2f}]")
                print(
                    f"    Outliers encontrados: {n_outliers} ({n_outliers / len(self.df) * 100:.1f}%)"
                )

    def graficar_hist(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        numericas = self.df_info.get(
            "numericas", self.df.select_dtypes(include=[np.number]).columns.tolist()
        )

        if not numericas:
            print("  No hay variables numéricas")
            return

        print(f"\n📊 Histograma")
        print(f"  Variables disponibles: {numericas[:5]}")
        col = input("  Variable: ").strip()

        if col not in self.df.columns:
            print(f"❌ Columna '{col}' no encontrada")
            return

        try:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(self.df[col].dropna(), bins=30, edgecolor="black", alpha=0.7)
            ax.set_xlabel(col)
            ax.set_ylabel("Frecuencia")
            ax.set_title(f"Histograma de {col}")
            plt.tight_layout()
            plt.savefig(f"histograma_{col}.png", dpi=100)
            print(f"  ✅ Guardado: histograma_{col}.png")
            plt.close()
        except Exception as e:
            print(f"❌ Error: {e}")

    def graficar_boxplot(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        numericas = self.df_info.get(
            "numericas", self.df.select_dtypes(include=[np.number]).columns.tolist()
        )

        print(f"\n📦 Boxplot")
        print(f"  Variables: {numericas[:5]}")
        col = input("  Variable: ").strip()

        if col not in self.df.columns:
            print(f"❌ Columna '{col}' no encontrada")
            return

        try:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.boxplot(self.df[col].dropna())
            ax.set_ylabel(col)
            ax.set_title(f"Boxplot de {col}")
            plt.tight_layout()
            plt.savefig(f"boxplot_{col}.png", dpi=100)
            print(f"  ✅ Guardado: boxplot_{col}.png")
            plt.close()
        except Exception as e:
            print(f"❌ Error: {e}")

    def graficar_scatter(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        numericas = self.df_info.get(
            "numericas", self.df.select_dtypes(include=[np.number]).columns.tolist()
        )

        if len(numericas) < 2:
            print("  Se necesitan al menos 2 variables numéricas")
            return

        print(f"\n📈 Scatter Plot")
        print(f"  Variables: {numericas}")
        x = input("  Variable X: ").strip()
        y = input("  Variable Y: ").strip()

        if x not in self.df.columns or y not in self.df.columns:
            print("❌ Columnas no encontradas")
            return

        try:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(self.df[x], self.df[y], alpha=0.5)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"{x} vs {y}")
            plt.tight_layout()
            plt.savefig(f"scatter_{x}_{y}.png", dpi=100)
            print(f"  ✅ Guardado: scatter_{x}_{y}.png")
            plt.close()
        except Exception as e:
            print(f"❌ Error: {e}")

    def analisis_categorico(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        categoricas = self.df_info.get(
            "categoricas", self.df.select_dtypes(include=["object"]).columns.tolist()
        )

        if not categoricas:
            print("  No hay variables categóricas")
            return

        print(f"\n🏷️ Análisis de Variables Categóricas")
        print(f"  Variables: {categoricas}")
        col = input("  Variable: ").strip()

        if col not in self.df.columns:
            print(f"❌ Columna '{col}' no encontrada")
            return

        print(f"\n  Valores únicos: {self.df[col].nunique()}")
        print("\n  Frecuencias:")
        freq = self.df[col].value_counts().head(10)
        for val, count in freq.items():
            pct = count / len(self.df) * 100
            print(f"    {val}: {count} ({pct:.1f}%)")

    def resumen_eda(self):
        if self.df is None:
            print("❌ No hay dataset")
            return

        print("""
╔═══════════════════════════════════════════════════════════╗
║              RESUMEN EDA COMPLETO                        ║
╚═══════════════════════════════════════════════════════════╝
        """)

        self.mostrar_shape()
        self.mostrar_dtypes()
        self.mostrar_describe()
        self.mostrar_nulos()

        numericas = self.df_info.get("numericas", [])
        if len(numericas) >= 2:
            print("\n🔗 Principales correlaciones:")
            corr = self.df[numericas].corr().abs()
            corr = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
            top_corr = corr.stack().nlargest(3)
            for (c1, c2), val in top_corr.items():
                print(f"    {c1} ↔ {c2}: {val:.3f}")

        print("\n✅ Resumen EDA completado")

    def ejecutar(self):
        """Loop principal del agente"""
        self.saludar()
        self.mostrar_ayuda()

        while True:
            try:
                cmd = input("\n🔹 EDA > ").strip().lower()

                if cmd in ["/salir", "/exit", "salir"]:
                    print("\n👋 ¡Hasta luego!")
                    break
                elif cmd == "/ayuda":
                    self.mostrar_ayuda()
                elif cmd == "/cargar":
                    self.cargar_dataset()
                elif cmd == "/info":
                    self.mostrar_info()
                elif cmd == "/head":
                    self.mostrar_head()
                elif cmd == "/tail":
                    self.mostrar_tail()
                elif cmd == "/shape":
                    self.mostrar_shape()
                elif cmd == "/dtypes":
                    self.mostrar_dtypes()
                elif cmd == "/describe":
                    self.mostrar_describe()
                elif cmd == "/nulos":
                    self.mostrar_nulos()
                elif cmd == "/correlacion":
                    self.mostrar_correlacion()
                elif cmd == "/outliers":
                    self.detectar_outliers()
                elif cmd == "/hist":
                    self.graficar_hist()
                elif cmd == "/boxplot":
                    self.graficar_boxplot()
                elif cmd == "/scatter":
                    self.graficar_scatter()
                elif cmd == "/categorico":
                    self.analisis_categorico()
                elif cmd == "/resumen":
                    self.resumen_eda()
                elif cmd:
                    print(f"  Comando '{cmd}' no reconocido. Usa /ayuda")

            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    agent = EDAAgent()
    agent.ejecutar()
