from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

def generar_analisis_festivo():
    """
    Función que genera el análisis de ventas del período festivo (22-31 Dic 2024)
    """
    # ========================= CARGA DE DATOS =========================
    df = pd.read_csv(BASE_DIR / "datos" / "sales_sample_2024.csv")
    df['sales_date'] = pd.to_datetime(df['sales_date'])

    # Filtrar período festivo
    df_festivos = df[(df['sales_date'] >= '2024-12-22') & 
                     (df['sales_date'] <= '2024-12-31')].copy()

    df_festivos = df_festivos.sort_values('sales_date').reset_index(drop=True)

    # ========================= CÁLCULOS =========================
    df_festivos['delta_diario'] = df_festivos['sales_amount'].diff()
    df_festivos['variacion_pct'] = df_festivos['delta_diario'] / df_festivos['sales_amount'].shift(1) * 100
    df_festivos['MA3'] = df_festivos['sales_amount'].rolling(window=3).mean()

    # ========================= GRÁFICO =========================
    fig, ax = plt.subplots(figsize=(15, 8))

    ax.plot(df_festivos['sales_date'], df_festivos['sales_amount'], 
            marker='o', linewidth=3, color='#1f77b4', label='Ventas Diarias', markersize=7)

    ax.plot(df_festivos['sales_date'], df_festivos['MA3'], 
            linewidth=2.5, linestyle='--', color='#ff7f0e', label='Promedio Móvil 3 días')

    ax.set_title('Evolución de Ventas - Período Festivo\n22 al 31 de Diciembre 2024', 
                 fontsize=18, fontweight='bold')
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Monto de Ventas ($)', fontsize=12)

    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    ax.legend(fontsize=11, loc='upper left')

    # Anotaciones
    for i, row in df_festivos.iterrows():
        if abs(row['variacion_pct']) > 8:
            color = 'green' if row['delta_diario'] > 0 else 'red'
            ax.annotate(f"{row['variacion_pct']:+.1f}%", 
                        xy=(row['sales_date'], row['sales_amount']),
                        xytext=(0, 18 if row['delta_diario'] > 0 else -25),
                        textcoords='offset points',
                        ha='center', fontsize=10.5, 
                        color=color, fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color=color, alpha=0.7))

    plt.tight_layout()

    # Guardar imagen
    nombre_imagen = BASE_DIR / "resultados" / "Evolucion_Ventas_Festivas_2024.png"
    plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')
    plt.close()

    return df_festivos


# ===================== EJECUCIÓN =====================
if __name__ == "__main__":
    generar_analisis_festivo()