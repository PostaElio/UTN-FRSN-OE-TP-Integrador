from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent


def generar_analisis_descriptivo():
    df = pd.read_csv(
        BASE_DIR / "datos" / "sales_sample_2024.csv",
        parse_dates=["sales_date"]
    )
    df = df.sort_values("sales_date").reset_index(drop=True)

    ventas = df["sales_amount"]

    # ========================= ESTADÍSTICAS =========================
    media    = ventas.mean()
    mediana  = ventas.median()
    minimo   = ventas.min()
    maximo   = ventas.max()
    std      = ventas.std()
    q1       = ventas.quantile(0.25)
    q3       = ventas.quantile(0.75)
    iqr      = q3 - q1
    lim_inf  = q1 - 1.5 * iqr
    lim_sup  = q3 + 1.5 * iqr
    outliers = df[(ventas < lim_inf) | (ventas > lim_sup)]

    # ========================= FIGURA =========================
    fig = plt.figure(figsize=(16, 10))
    gs  = fig.add_gridspec(2, 2, hspace=0.45, wspace=0.30)

    ax_hist = fig.add_subplot(gs[0, 0])
    ax_box  = fig.add_subplot(gs[0, 1])
    ax_time = fig.add_subplot(gs[1, :])

    # --- Histograma ---
    ax_hist.hist(ventas, bins=20, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax_hist.axvline(media,   color="#E53935", linestyle="--", linewidth=1.6,
                   label=f"Media: ${media:,.0f}")
    ax_hist.axvline(mediana, color="#FF8F00", linestyle="--", linewidth=1.6,
                   label=f"Mediana: ${mediana:,.0f}")
    ax_hist.set_title("Distribución de Montos de Venta", fontweight="bold", fontsize=12)
    ax_hist.set_xlabel("Monto de Venta ($)", fontsize=10)
    ax_hist.set_ylabel("Frecuencia", fontsize=10)
    ax_hist.legend(fontsize=9)
    ax_hist.grid(axis="y", alpha=0.3)

    # --- Boxplot ---
    ax_box.boxplot(
        ventas,
        patch_artist=True,
        widths=0.5,
        boxprops=dict(facecolor="#4C72B0", alpha=0.7),
        medianprops=dict(color="#FF8F00", linewidth=2.2),
        whiskerprops=dict(linewidth=1.5),
        capprops=dict(linewidth=1.5),
        flierprops=dict(marker="o", markerfacecolor="#E53935",
                        markersize=5, alpha=0.7, linestyle="none"),
    )
    ax_box.set_title("Diagrama de Caja — Detección de Outliers", fontweight="bold", fontsize=12)
    ax_box.set_ylabel("Monto de Venta ($)", fontsize=10)
    ax_box.set_xticks([])
    ax_box.grid(axis="y", alpha=0.3)

    stats_text = (
        f"Mín:      ${minimo:,.0f}\n"
        f"Q1:       ${q1:,.0f}\n"
        f"Mediana: ${mediana:,.0f}\n"
        f"Q3:       ${q3:,.0f}\n"
        f"Máx:      ${maximo:,.0f}\n"
        f"IQR:      ${iqr:,.0f}\n"
        f"Desv. Est: ${std:,.0f}\n"
        f"Outliers:  {len(outliers)}"
    )
    ax_box.text(
        1.38, mediana, stats_text,
        fontsize=9, va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFFDE7",
                  edgecolor="gray", alpha=0.9)
    )

    # --- Serie temporal ---
    ax_time.plot(
        df["sales_date"], df["sales_amount"],
        color="#4C72B0", linewidth=1.1, alpha=0.75, label="Ventas diarias"
    )
    ax_time.axhline(
        media, color="#E53935", linestyle="--", linewidth=1.4,
        label=f"Media: ${media:,.0f}"
    )
    ax_time.fill_between(
        df["sales_date"], media - std, media + std,
        alpha=0.10, color="#E53935", label=f"±1 Desv. Est. (${std:,.0f})"
    )
    ax_time.scatter(
        outliers["sales_date"], outliers["sales_amount"],
        color="#E53935", zorder=5, s=45,
        label=f"Outliers ({len(outliers)})"
    )
    ax_time.set_title("Evolución Temporal de Ventas — 2024", fontweight="bold", fontsize=12)
    ax_time.set_xlabel("Fecha", fontsize=10)
    ax_time.set_ylabel("Monto de Venta ($)", fontsize=10)
    ax_time.legend(fontsize=9, loc="upper left")
    ax_time.grid(alpha=0.3)

    fig.suptitle(
        "Análisis Descriptivo de Ventas — 2024",
        fontsize=15, fontweight="bold"
    )

    plt.tight_layout()
    out_path = BASE_DIR / "resultados" / "analisis_descriptivo_ventas_2024.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    generar_analisis_descriptivo()
