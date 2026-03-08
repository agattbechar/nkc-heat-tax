"""
src/analysis/04_clean_temperature.py
Clean raw hourly data → two processed outputs:
  1. temp_hourly.csv   — filtered to working hours (08:00–18:00)
  2. temp_monthly.csv  — hours per month above each threshold

Run after: 01_get_temperature.py
"""

import pandas as pd
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
WORKING_HOUR_START = 8
WORKING_HOUR_END   = 18
THRESHOLDS         = [35, 38, 40, 42, 44]

RAW_PATH      = Path(__file__).resolve().parents[2] / "data" / "raw" / "temperature" / "nouakchott_hourly_all.csv"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

MONTHS_FR = {
    1:"Jan", 2:"Fév", 3:"Mar", 4:"Avr",
    5:"Mai", 6:"Jui", 7:"Jul", 8:"Aoû",
    9:"Sep", 10:"Oct", 11:"Nov", 12:"Déc"
}


def main():
    print("Loading raw data...")
    df = pd.read_csv(RAW_PATH, parse_dates=["datetime"])
    print(f"  {len(df):,} rows loaded")

    # ── Filter to working hours ───────────────────────────────────────────────
    working = df[
        (df["hour"] >= WORKING_HOUR_START) &
        (df["hour"] <  WORKING_HOUR_END)
    ].copy()
    working.to_csv(PROCESSED_DIR / "temp_hourly.csv", index=False)
    print(f"  Working hours only: {len(working):,} rows → temp_hourly.csv")

    # ── Monthly aggregation ───────────────────────────────────────────────────
    records = []
    for (year, month), group in working.groupby(["year", "month"]):
        rec = {
            "year":        year,
            "month":       month,
            "month_label": MONTHS_FR[month],
            "total_hours": len(group),
            "mean_temp_c": round(group["temp_c"].mean(), 2),
            "max_temp_c":  round(group["temp_c"].max(), 2),
        }
        for t in THRESHOLDS:
            count = int((group["temp_c"] >= t).sum())
            rec[f"hours_above_{t}c"] = count
            rec[f"pct_above_{t}c"]   = round(count / len(group) * 100, 1)
        records.append(rec)

    monthly = pd.DataFrame(records).sort_values(["year", "month"])
    monthly.to_csv(PROCESSED_DIR / "temp_monthly.csv", index=False)
    print(f"  Monthly summary → temp_monthly.csv")

    # ── Print overview ────────────────────────────────────────────────────────
    avg = monthly.groupby("month").agg(
        label        = ("month_label",     "first"),
        mean_temp    = ("mean_temp_c",     "mean"),
        hrs_above_35 = ("hours_above_35c", "mean"),
        hrs_above_38 = ("hours_above_38c", "mean"),
        hrs_above_42 = ("hours_above_42c", "mean"),
    ).reset_index()

    print(f"\n── Average working hours above threshold (all years) ────────")
    print(f"{'':4s}  {'Avg°C':>6}  {'>35°C':>6}  {'>38°C':>6}  {'>42°C':>6}  compression")
    print(f"{'':4s}  {'──────':>6}  {'──────':>6}  {'──────':>6}  {'──────':>6}")
    for _, r in avg.iterrows():
        total = 10  # working hours window (08–18)
        bar = "█" * int(r["hrs_above_38"] / 4)
        print(
            f"{r['label']:4s}  "
            f"{r['mean_temp']:>6.1f}  "
            f"{r['hrs_above_35']:>6.0f}h  "
            f"{r['hrs_above_38']:>6.0f}h  "
            f"{r['hrs_above_42']:>6.0f}h  "
            f"{bar}"
        )

    print("\nDone. data/processed/ ready.")


if __name__ == "__main__":
    main()