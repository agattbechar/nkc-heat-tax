# src/visualization/09_chart_activity_curve.py
"""
Chart 1: Temperature vs Work Capacity
The ILO/ISO curve applied — shows the inflection point.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from visualization.chart_style import apply, RED, GREY_MID, GREY_LIGHT, BLACK, GREY_DARK

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
CHARTS_DIR    = Path(__file__).resolve().parents[2] / "site" / "assets" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ILO/ISO curve points
CURVE = [
    (0,  1.00), (24, 1.00), (26, 0.95), (28, 0.88),
    (30, 0.80), (32, 0.70), (33, 0.60), (34, 0.50),
    (36, 0.40), (38, 0.30), (40, 0.20), (42, 0.10),
    (44, 0.05), (50, 0.05),
]

def main():
    apply()
    temps = [p[0] for p in CURVE]
    caps  = [p[1] * 100 for p in CURVE]
    t_smooth = np.linspace(0, 48, 500)
    c_smooth = np.interp(t_smooth, temps, caps)

    fig, ax = plt.subplots(figsize=(9, 5))

    # Shade zones
    ax.axvspan(0,  28, alpha=0.04, color="blue",  zorder=0)
    ax.axvspan(28, 34, alpha=0.04, color="orange", zorder=0)
    ax.axvspan(34, 48, alpha=0.06, color=RED,      zorder=0)

    # The curve
    ax.plot(t_smooth, c_smooth, color=RED, linewidth=2.5, zorder=3)

    # Nouakchott reference lines
    ax.axvline(24.5, color=GREY_MID, linewidth=1, linestyle="--", alpha=0.7)
    ax.axvline(32.5, color=RED,      linewidth=1, linestyle="--", alpha=0.7)

    ax.text(24.5, 8, "Jan\n24.5°C", ha="center", fontsize=9,
            color=GREY_MID, style="italic")
    ax.text(32.5, 8, "Oct\n32.5°C", ha="center", fontsize=9,
            color=RED, style="italic")

    # 50% mark
    ax.axhline(50, color=GREY_LIGHT, linewidth=1, linestyle=":", zorder=1)
    ax.text(1, 51, "50% capacity", fontsize=8, color=GREY_DARK, va="bottom")

    # Labels
    ax.set_xlabel("Température (°C) / Temperature (°C)")
    ax.set_ylabel("Capacité de travail (%) / Work Capacity (%)")
    ax.set_title(
        "Courbe de capacité de travail par température\n"
        "Work Capacity by Temperature — ILO/ISO Standard (moderate intensity)",
        pad=12
    )
    ax.set_xlim(0, 48)
    ax.set_ylim(0, 110)
    ax.set_xticks(range(0, 50, 4))

    # Zone labels
    ax.text(14,  105, "Normal",    ha="center", fontsize=8, color=GREY_DARK)
    ax.text(31,  105, "Stress",    ha="center", fontsize=8, color="darkorange")
    ax.text(41,  105, "Critique",  ha="center", fontsize=8, color=RED)

    # Source
    fig.text(0.01, 0.01, "Source: ILO (2019) Working on a Warmer Planet; ISO 7243:2017",
             fontsize=7, color=GREY_MID)

    path = CHARTS_DIR / "activity_curve.png"
    plt.savefig(path)
    plt.close()
    print(f"Saved → {path.name}")

if __name__ == "__main__":
    main()