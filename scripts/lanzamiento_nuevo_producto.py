from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin ventana, solo genera archivos
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE_DIR = Path(__file__).resolve().parent.parent


def generar():
    csv_path = BASE_DIR / "datos" / "sales_sample_2024.csv"
    df = pd.read_csv(csv_path, parse_dates=["sales_date"])

    # Semana de análisis: lunes 18/03 al domingo 24/03 (semana 12)
    # Lanzamiento del nuevo producto: miércoles 20/03/2024
    WEEK_START = pd.Timestamp("2024-03-18")
    WEEK_END   = pd.Timestamp("2024-03-24")

    # Filtrar solo esa semana
    mask = (df["sales_date"] >= WEEK_START) & (df["sales_date"] <= WEEK_END)
    week_df = df[mask].copy()

    # Agrupar por día y rellenar días sin datos con 0
    daily = (
        week_df.groupby("sales_date")["sales_amount"]
        .sum()
        .reindex(pd.date_range(WEEK_START, WEEK_END), fill_value=0)
    )

    day_labels_es = ["Lun 18/03", "Mar 19/03", "Mié 20/03\n★ Lanzamiento",
                     "Jue 21/03", "Vie 22/03", "Sáb 23/03", "Dom 24/03"]

    ventas = daily.values

    # Colores: pre-lanzamiento gris, lanzamiento rojo/destacado, post-lanzamiento azul, fin de semana naranja
    colors = [
        "#9E9E9E",   # Lunes  - pre-lanzamiento
        "#9E9E9E",   # Martes - pre-lanzamiento
        "#E53935",   # Miércoles - LANZAMIENTO (rojo destacado)
        "#4C72B0",   # Jueves - post-lanzamiento
        "#4C72B0",   # Viernes - post-lanzamiento
        "#DD8452",   # Sábado - fin de semana
        "#DD8452",   # Domingo - fin de semana
    ]

    fig, ax = plt.subplots(figsize=(11, 6))

    bars = ax.bar(day_labels_es, ventas, color=colors, edgecolor="white", width=0.6, zorder=3)

    for bar, val in zip(bars, ventas):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 100,
            f"${val:,.0f}",
            ha="center", va="bottom", fontsize=9, fontweight="bold"
        )

    avg = ventas.mean()
    ax.axhline(avg, color="gray", linestyle="--", linewidth=1.3, zorder=2,
               label=f"Promedio semanal: ${avg:,.0f}")

    launch_bar = bars[2]
    ax.annotate(
        "Lanzamiento\ndel producto",
        xy=(launch_bar.get_x() + launch_bar.get_width() / 2, launch_bar.get_height()),
        xytext=(launch_bar.get_x() + launch_bar.get_width() / 2 + 0.6, launch_bar.get_height() - 1200),
        fontsize=9, color="#B71C1C", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.5),
        ha="left"
    )

    patch_pre    = mpatches.Patch(color="#9E9E9E", label="Pre-lanzamiento")
    patch_launch = mpatches.Patch(color="#E53935", label="Día de lanzamiento (Mié 20/03)")
    patch_post   = mpatches.Patch(color="#4C72B0", label="Post-lanzamiento (días hábiles)")
    patch_wknd   = mpatches.Patch(color="#DD8452", label="Fin de semana")
    avg_line     = plt.Line2D([0], [0], color="gray", linestyle="--", linewidth=1.3,
                              label=f"Promedio semanal: ${avg:,.0f}")
    ax.legend(handles=[patch_pre, patch_launch, patch_post, patch_wknd, avg_line],
              fontsize=8.5, loc="upper right")

    ax.set_title(
        "Ventas diarias — Semana 12 (18/03/2024 al 24/03/2024)\n"
        "Impacto del lanzamiento del nuevo producto (miércoles 20/03)",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.set_xlabel("Día de la semana", fontsize=11)
    ax.set_ylabel("Ventas ($)", fontsize=11)
    ax.set_ylim(0, max(ventas) * 1.20)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

    plt.tight_layout()
    out_path = BASE_DIR / "resultados" / "ventas_semana12_lanzamiento.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Gráfico guardado en: {out_path}")


if __name__ == "__main__":
    generar()
