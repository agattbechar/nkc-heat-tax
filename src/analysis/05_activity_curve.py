"""
src/analysis/05_activity_curve.py

Apply ILO/ISO work capacity curve to hourly temperature data.
No behavioral data needed — the international standard is the curve.

Methodology:
  ILO "Working on a Warmer Planet" (2019) + ISO 7243
  Work capacity reduction by dry bulb temperature, moderate work intensity.
  Moderate intensity = market vendors, construction workers, port workers.

Input:  data/processed/temp_hourly.csv
Output: data/processed/work_capacity_hourly.csv
        data/processed/work_capacity_monthly.csv

Citations:
  - ILO (2019). Working on a Warmer Planet. Geneva: ILO.
  - ISO 7243:2017. Ergonomics of the thermal environment.
  - ISO 7933:2004. Ergonomics — Analytical determination of heat stress.
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

MONTHS_FR = {
    1:"Jan", 2:"Fév", 3:"Mar", 4:"Avr",
    5:"Mai", 6:"Jui", 7:"Jul", 8:"Aoû",
    9:"Sep", 10:"Oct", 11:"Nov", 12:"Déc"
}

# ── ILO/ISO Work Capacity Curve ───────────────────────────────────────────────
# Source: ILO "Working on a Warmer Planet" (2019), Table 2
#         ISO 7243:2017 — moderate work intensity (200–300W metabolic rate)
# Format: (temp_threshold, work_capacity_pct)
# Linear interpolation between breakpoints.
#
# ASSUMPTION: Moderate work intensity — representative of:
#   - Market vendors (standing, carrying light loads)
#   - Construction workers (masonry, carrying materials)
#   - Port workers (loading, sorting)
# See docs/assumptions.md for full rationale.

WORK_CAPACITY_CURVE = [
    (0,   1.00),   # below 24°C — full capacity
    (24,  1.00),
    (26,  0.95),
    (28,  0.88),
    (30,  0.80),
    (32,  0.70),
    (33,  0.60),
    (34,  0.50),   # ILO: 50% capacity at 33–34°C
    (36,  0.40),
    (38,  0.30),   # significant heat stress
    (40,  0.20),
    (42,  0.10),   # ISO 7933: near work stop threshold
    (44,  0.05),
    (50,  0.05),   # floor — some activity always present
]

TEMPS   = [p[0] for p in WORK_CAPACITY_CURVE]
CAPS    = [p[1] for p in WORK_CAPACITY_CURVE]


def work_capacity(temp_c: float) -> float:
    """Interpolate work capacity from ILO/ISO curve."""
    return float(np.interp(temp_c, TEMPS, CAPS))


def main():
    print("Starting...")
    path = PROCESSED_DIR / "temp_hourly.csv"
    print(f"Looking for: {path}")
    print(f"Exists: {path.exists()}")
    
    print("Loading temp_hourly.csv...")
    df = pd.read_csv(PROCESSED_DIR / "temp_hourly.csv", parse_dates=["datetime"])
    ...
    # ── Apply curve to every hour ─────────────────────────────────────────────
    df["work_capacity"] = df["temp_c"].apply(work_capacity)
    df["hours_lost"]    = 1 - df["work_capacity"]

    # Save hourly
    df.to_csv(PROCESSED_DIR / "work_capacity_hourly.csv", index=False)
    print(f"  Saved → work_capacity_hourly.csv")

    # ── Monthly aggregation ───────────────────────────────────────────────────
    records = []
    for (year, month), g in df.groupby(["year", "month"]):
        total_hours     = len(g)
        full_capacity   = total_hours * 1.0
        actual_capacity = g["work_capacity"].sum()
        hours_lost      = total_hours - actual_capacity

        records.append({
            "year":                  year,
            "month":                 month,
            "month_label":           MONTHS_FR[month],
            "total_working_hours":   total_hours,
            "mean_temp_c":           round(g["temp_c"].mean(), 2),
            "mean_work_capacity":    round(g["work_capacity"].mean(), 4),
            "effective_hours":       round(actual_capacity, 1),
            "hours_lost":            round(hours_lost, 1),
            "compression_pct":       round(hours_lost / full_capacity * 100, 1),
        })

    monthly = pd.DataFrame(records).sort_values(["year", "month"])
    monthly.to_csv(PROCESSED_DIR / "work_capacity_monthly.csv", index=False)
    print(f"  Saved → work_capacity_monthly.csv")

    # ── Average by month across all years ────────────────────────────────────
    avg = monthly.groupby("month").agg(
        label            = ("month_label",       "first"),
        mean_temp        = ("mean_temp_c",        "mean"),
        mean_capacity    = ("mean_work_capacity", "mean"),
        avg_hours_lost   = ("hours_lost",         "mean"),
        avg_compression  = ("compression_pct",    "mean"),
    ).reset_index()

    print(f"\n── Average monthly work capacity (all years) ────────────────")
    print(f"{'':4s}  {'Avg°C':>6}  {'Capacity':>9}  {'Hrs lost':>9}  {'Loss%':>6}  bar")
    print(f"{'':4s}  {'──────':>6}  {'─────────':>9}  {'─────────':>9}  {'──────':>6}")
    for _, r in avg.iterrows():
        bar = "█" * int(r["avg_compression"] / 3)
        print(
            f"{r['label']:4s}  "
            f"{r['mean_temp']:>6.1f}  "
            f"{r['mean_capacity']*100:>8.1f}%  "
            f"{r['avg_hours_lost']:>8.1f}h  "
            f"{r['avg_compression']:>5.1f}%  "
            f"{bar}"
        )

    # ── Annual summary ────────────────────────────────────────────────────────
    annual = monthly.groupby("year").agg(
        total_hours      = ("total_working_hours", "sum"),
        effective_hours  = ("effective_hours",     "sum"),
        hours_lost       = ("hours_lost",          "sum"),
    ).reset_index()
    annual["compression_pct"] = round(
        annual["hours_lost"] / annual["total_hours"] * 100, 1
    )
    annual["capacity_pct"] = 100 - annual["compression_pct"]

    print(f"\n── Annual summary ───────────────────────────────────────────")
    print(f"{'Year':>6}  {'Total hrs':>10}  {'Effective':>10}  {'Lost':>8}  {'Capacity':>9}")
    print(f"{'──────':>6}  {'──────────':>10}  {'──────────':>10}  {'────────':>8}  {'─────────':>9}")
    for _, r in annual.iterrows():
        print(
            f"{int(r['year']):>6}  "
            f"{r['total_hours']:>10,.0f}  "
            f"{r['effective_hours']:>10,.0f}  "
            f"{r['hours_lost']:>8,.0f}  "
            f"{r['capacity_pct']:>8.1f}%"
        )

    overall_capacity = (
        annual["effective_hours"].sum() / annual["total_hours"].sum() * 100
    )
    print(f"\n  → Nouakchott runs at {overall_capacity:.1f}% of potential (2019–2025)")
    print(f"  → Annual heat compression: {100 - overall_capacity:.1f}%")


if __name__ == "__main__":
    main()