"""
Custom Agent para PYMESML

Agente conversacional para gestión de stock y predicción de demanda.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.pipelines.business import GestorStockPipeline
from src.pipelines.ml import MLPipeline, PredictorDemandaPipeline
import pandas as pd


class PYMESMLAgent:
    """Agente conversacional para Investigación Operativa"""

    COMANDOS = {
        "eoq": "Calcular EOQ clásico",
        "eoq_faltantes": "EOQ con backorders",
        "eoq_descuentos": "EOQ con descuentos por volumen",
        "eoq_produccion": "EOQ de producción",
        "abc": "Clasificación ABC",
        "predecir": "Entrenar modelo ML",
        "generar": "Generar datos sintéticos",
        "ayuda": "Mostrar ayuda",
        "salir": "Terminar",
    }

    def __init__(self):
        self.modelo_entrenado = None
        self.demanda_data = None

    def saludar(self):
        print("""
╔═══════════════════════════════════════════════════════════╗
║           PYMESML Agent - Tu Asistente de IO            ║
╠═══════════════════════════════════════════════════════════╣
║  Puedo ayudarte con:                                    ║
║  • Cálculos EOQ (clásico, faltantes, descuentos, prod)  ║
║  • Clasificación ABC de inventarios                      ║
║  • Predicción de demanda con Machine Learning            ║
║  • Generación de series temporales                       ║
╚═══════════════════════════════════════════════════════════╝
        """)

    def mostrar_ayuda(self):
        print("\n📋 Comandos disponibles:")
        for cmd, desc in self.COMANDOS.items():
            print(f"  /{cmd:<15} → {desc}")

    def run_eoq_clasico(self):
        print("\n📦 EOQ Clásico")
        try:
            D = float(input("  Demanda anual: "))
            C1 = float(input("  Costo almacenamiento ($): "))
            C3 = float(input("  Costo ordenamiento ($): "))
            C4 = float(input("  Costo unitario (opcional): ") or 0)
            lead = float(input("  Lead time días (opcional): ") or 0)

            r = GestorStockPipeline.eoq_clasico(D, C1, C3, C4, lead)

            print(f"""
┌─────────── Resultados ───────────┐
│ Q* Óptimo:        {r.Q_optimo:>10.2f} unidades │
│ Costo Total:      {r.costo_total:>10.2f}       │
│ Pedidos/Año:      {r.numero_pedidos:>10.2f}       │
│ Ciclo:            {r.ciclo_dias:>10.1f} días     │
│ Punto Reorden:    {r.punto_reorden:>10.1f} unidades │
└──────────────────────────────────┘
            """)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def run_eoq_faltantes(self):
        print("\n⚠️ EOQ con Faltantes")
        try:
            D = float(input("  Demanda anual: "))
            C1 = float(input("  Costo almacenamiento: "))
            C2 = float(input("  Costo faltante: "))
            C3 = float(input("  Costo ordenamiento: "))

            r = GestorStockPipeline.eoq_faltantes(D, C1, C2, C3)

            print(f"""
┌─────────── Resultados ───────────┐
│ Q* Óptimo:        {r["Q_optimo"]:>10.2f} unidades │
│ Faltantes Máx:    {r["S_max"]:>10.2f} unidades │
│ Inventario Máx:   {r["I_maximo"]:>10.2f} unidades │
│ Costo Total:      {r["costo_total"]:>10.2f}       │
└──────────────────────────────────┘
            """)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def run_eoq_descuentos(self):
        print("\n💰 EOQ con Descuentos")
        try:
            D = float(input("  Demanda anual: "))
            C3 = float(input("  Costo ordenamiento: "))
            i = float(input("  Tasa mantención (0.1 = 10%): "))

            n = int(input("  Número de rangos de precio: "))
            rangos = []
            for j in range(n):
                print(f"  Rangos {j + 1}:")
                mn = int(input("    Min: "))
                mx = int(input("    Max: "))
                pr = float(input("    Precio: "))
                rangos.append({"min": mn, "max": mx, "precio": pr})

            r = GestorStockPipeline.eoq_descuentos(D, C3, i, rangos)

            print(f"""
┌─────────── Mejor Opción ───────────┐
│ Q* Óptimo:        {r["Q_optimo"]:>10.0f} unidades │
│ Precio Unitario:  {r["precio_unitario"]:>10.2f}       │
│ Costo Total:      {r["costo_total"]:>10.2f}       │
└─────────────────────────────────────┘
            """)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def run_eoq_produccion(self):
        print("\n🏭 EOQ de Producción")
        try:
            D = float(input("  Demanda anual: "))
            C1 = float(input("  Costo almacenamiento: "))
            C3 = float(input("  Costo preparación: "))
            d = float(input("  Tasa demanda: "))
            p = float(input("  Tasa producción: "))

            r = GestorStockPipeline.eoq_produccion(D, C1, C3, d, p)

            print(f"""
┌─────────── Resultados ───────────┐
│ Q* Lote:           {r["Q_optimo"]:>10.0f} unidades │
│ Inventario Máx:    {r["I_maximo"]:>10.0f} unidades │
│ Costo Total:       {r["costo_total"]:>10.2f}       │
│ Tiempo Prod:       {r["tiempo_produccion_dias"]:>10.1f} días     │
└──────────────────────────────────┘
            """)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def run_abc(self):
        print("\n📊 Clasificación ABC")
        archivo = input("  Ruta archivo CSV: ")
        if not os.path.exists(archivo):
            print("❌ Archivo no encontrado")
            return

        try:
            df = pd.read_csv(archivo)
            print(f"  Columnas disponibles: {list(df.columns)}")
            col = input("  Columna de valor: ")
            a = float(input("  Umbral A% (default 80): ") or 80) / 100
            b = float(input("  Umbral B% (default 95): ") or 95) / 100

            res, stats = GestorStockPipeline.abc(df, col, a, b)

            print(f"""
┌─────────── Clasificación ABC ───────────┐
{res[["clase", col]].groupby("clase").sum().to_string()}
└──────────────────────────────────────────┘
            """)
            print("\nEstadísticas por clase:")
            print(stats)
        except Exception as e:
            print(f"❌ Error: {e}")

    def run_generar_datos(self):
        print("\n📈 Generar Datos de Demanda")
        try:
            n = int(input("  Días: ") or 365)
            t = float(input("  Tendencia: ") or 0.5)
            e = float(input("  Estacionalidad: ") or 15)
            r = float(input("  Ruido: ") or 5)

            self.demanda_data = PredictorDemandaPipeline.generar(n, t, e, r)
            print(f"\n✅ Generados {len(self.demanda_data)} registros")
            print(self.demanda_data.head())
        except Exception as e:
            print(f"❌ Error: {e}")

    def run_predecir(self):
        print("\n🤖 Entrenar Modelo de Predicción")
        if self.demanda_data is None:
            print("❌ Primero genera datos con /generar")
            return

        try:
            print("  Modelos: lineal, ridge, rf, gb")
            m = input("  Modelo: ") or "lineal"
            feats = input("  Features (separados por coma): ").split(",") or [
                "dia",
                "mes",
            ]

            X = self.demanda_data[feats]
            y = self.demanda_data["demanda"]

            self.modelo_entrenado = MLPipeline(m.strip()).entrenar(X, y)
            print(f"\n✅ Modelo entrenado")
            print(f"   R²: {self.modelo_entrenado.r2:.4f}")
            print(f"   RMSE: {self.modelo_entrenado.rmse:.2f}")
            print(f"   MAE: {self.modelo_entrenado.mae:.2f}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def ejecutar(self):
        """Loop principal del agente"""
        self.saludar()
        self.mostrar_ayuda()

        while True:
            try:
                cmd = input("\n🔹 PYMESML > ").strip().lower()

                if cmd in ["/salir", "/exit", "salir"]:
                    print("\n👋 ¡Hasta luego!")
                    break
                elif cmd == "/ayuda":
                    self.mostrar_ayuda()
                elif cmd == "/eoq":
                    self.run_eoq_clasico()
                elif cmd == "/eoq_faltantes":
                    self.run_eoq_faltantes()
                elif cmd == "/eoq_descuentos":
                    self.run_eoq_descuentos()
                elif cmd == "/eoq_produccion":
                    self.run_eoq_produccion()
                elif cmd == "/abc":
                    self.run_abc()
                elif cmd == "/generar":
                    self.run_generar_datos()
                elif cmd == "/predecir":
                    self.run_predecir()
                elif cmd:
                    print(f"  Comando '{cmd}' no reconocido. Usa /ayuda")
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    agent = PYMESMLAgent()
    agent.ejecutar()
