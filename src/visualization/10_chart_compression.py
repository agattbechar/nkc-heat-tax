# src/visualization/10_chart_compression.py
"""
Chart 2: Monthly compression bar chart — hours lost per worker.
The October spike is the visual story.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from visualization.chart_style import apply, RED, RED_LIGHT, GREY_LIGHT, GREY_MID, BLACK

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
CHARTS_DIR    = Path(__file__).resolve().parents[2] / "site" / "assets" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    apply()
    df = pd.read_csv(PROCESSED_DIR / "compression_cost.csv")

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = [RED if row["compression_pct"] >= 30
              else RED_LIGHT if row["compression_pct"] >= 20
              else GREY_LIGHT
              for _, row in df.iterrows()]

    bars = ax.bar(df["month_label"], df["hours_lost"],
                  color=colors, width=0.7, zorder=2)

    # Annotate October
    oct_idx = df[df["month"] == 10].index[0]
    oct_val = df.loc[oct_idx, "hours_lost"]
    ax.annotate(
        f"Octobre\n{oct_val:.0f}h perdues",
        xy=(oct_idx, oct_val),
        xytext=(oct_idx - 1.5, oct_val + 5),
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
        fontsize=9, color=RED
    )

    # Annual total line
    annual = df["hours_lost"].sum()
    ax.text(0.98, 0.97,
            f"Total annuel / Annual total: {annual:.0f}h par travailleur / per worker",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color=GREY_MID,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor=GREY_LIGHT, alpha=0.8))

    ax.set_xlabel("Mois / Month")
    ax.set_ylabel("Heures perdues / Hours Lost")
    ax.set_title(
        "Heures de travail perdues à cause de la chaleur, par mois\n"
        "Working Hours Lost to Heat, by Month — Nouakchott average 2019–2025",
        pad=12
    )
    ax.set_ylim(0, df["hours_lost"].max() * 1.25)

    fig.text(0.01, 0.01,
             "Source: Open-Meteo 2019–2025; ILO (2019); ISO 7243:2017. "
             "Travailleur extérieur, intensité modérée / Outdoor worker, moderate intensity.",
             fontsize=7, color=GREY_MID)

    path = CHARTS_DIR / "compression.png"
    plt.savefig(path)
    plt.close()
    print(f"Saved → {path.name}")

if __name__ == "__main__":
    main()