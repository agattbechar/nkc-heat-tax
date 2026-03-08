# src/visualization/12_chart_shadow.py
"""
Chart 4: The shadow output — current vs potential.
The one number made visual.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from visualization.chart_style import apply, RED, GREY_LIGHT, GREY_MID, BLACK

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
CHARTS_DIR    = Path(__file__).resolve().parents[2] / "site" / "assets" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

MONTHS_FR = ["Jan","Fév","Mar","Avr","Mai","Jui",
             "Jul","Aoû","Sep","Oct","Nov","Déc"]

def main():
    apply()
    df = pd.read_csv(PROCESSED_DIR / "shadow_output.csv")

    fig, ax = plt.subplots(figsize=(11, 5.5))

    x      = range(12)
    full   = [100] * 12
    actual = df["work_capacity_pct"].tolist()
    lost   = [100 - a for a in actual]

    # Potential (background)
    ax.bar(x, full, color=GREY_LIGHT, width=0.7,
           label="Potentiel / Potential", zorder=1)

    # Actual capacity
    ax.bar(x, actual, color="#2C3E50", width=0.7,
           label="Capacité effective / Effective capacity", zorder=2)

    # Lost (overlay)
    ax.bar(x, lost, bottom=actual, color=RED, width=0.7,
           alpha=0.85, label="Perdu à la chaleur / Lost to heat", zorder=2)

    # The 80% line
    ax.axhline(80, color=RED, linewidth=1.2, linestyle="--", alpha=0.6, zorder=3)
    ax.text(11.4, 80.5, "80%", fontsize=9, color=RED, va="bottom", ha="right")

    # Annotate October
    ax.annotate(
        "Oct: 62%\ncapacité",
        xy=(9, 62), xytext=(7.5, 45),
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
        fontsize=9, color=RED
    )

    ax.set_xticks(x)
    ax.set_xticklabels(MONTHS_FR)
    ax.set_ylabel("Capacité de travail (%) / Work Capacity (%)")
    ax.set_ylim(0, 115)
    ax.set_title(
        "Production réelle vs. potentielle — La Taxe Canicule\n"
        "Actual vs. Potential Output — The Heat Tax — Nouakchott 2019–2025",
        pad=12
    )

    # Big number annotation
    ax.text(0.5, 0.92,
            "Nouakchott tourne à 80% de son potentiel  /  Nouakchott runs at 80% of potential",
            transform=ax.transAxes, ha="center", va="top",
            fontsize=10, color=BLACK,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=GREY_LIGHT, alpha=0.9))

    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)

    fig.text(0.01, 0.01,
             "Source: Open-Meteo 2019–2025; ILO (2019); ISO 7243:2017. "
             "Moyenne 2019–2025 / 2019–2025 average.",
             fontsize=7, color=GREY_MID)

    path = CHARTS_DIR / "shadow_output.png"
    plt.savefig(path)
    plt.close()
    print(f"Saved → {path.name}")

if __name__ == "__main__":
    main()