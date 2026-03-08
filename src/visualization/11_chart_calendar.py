# src/visualization/11_chart_calendar.py
"""
Chart 3: 12-month heat calendar heatmap.
Shows compression % by month and year — the full picture at a glance.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from visualization.chart_style import apply, GREY_MID

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
CHARTS_DIR    = Path(__file__).resolve().parents[2] / "site" / "assets" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

MONTHS_FR = ["Jan","Fév","Mar","Avr","Mai","Jui",
             "Jul","Aoû","Sep","Oct","Nov","Déc"]

def main():
    apply()
    df = pd.read_csv(PROCESSED_DIR / "work_capacity_monthly.csv")

    # Pivot: years × months
    pivot = df.pivot_table(
        index="year", columns="month",
        values="compression_pct", aggfunc="mean"
    )
    pivot.columns = MONTHS_FR

    fig, ax = plt.subplots(figsize=(12, 5))

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "heat", ["#FFFFFF", "#F5C6B0", "#C0392B"], N=256
    )

    im = ax.imshow(pivot.values, cmap=cmap, aspect="auto",
                   vmin=0, vmax=45)

    # Axis labels
    ax.set_xticks(range(12))
    ax.set_xticklabels(MONTHS_FR)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([str(y) for y in pivot.index])

    # Annotate cells
    for i in range(len(pivot.index)):
        for j in range(12):
            val = pivot.values[i, j]
            color = "white" if val > 28 else "#444444"
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                    fontsize=8, color=color)

    plt.colorbar(im, ax=ax, label="Compression (%)", shrink=0.8)

    ax.set_title(
        "Calendrier de compression thermique — Nouakchott\n"
        "Heat Compression Calendar — % of working capacity lost by month and year",
        pad=12
    )

    fig.text(0.01, 0.01,
             "Source: Open-Meteo 2019–2025; ILO (2019); ISO 7243:2017.",
             fontsize=7, color=GREY_MID)

    path = CHARTS_DIR / "calendar.png"
    plt.savefig(path)
    plt.close()
    print(f"Saved → {path.name}")

if __name__ == "__main__":
    main()