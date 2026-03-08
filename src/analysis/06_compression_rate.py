"""
src/analysis/06_compression_rate.py

Convert work capacity loss into monetary cost — in ouguiyas.
Applies wage estimates to hours lost per month.

Input:  data/processed/work_capacity_monthly.csv
Output: data/processed/compression_cost.csv

Wage anchor: SMIG 3,000 MRU/month (ILO 2022)
Using SMIG is a conservative lower bound — informal workers often earn more.
This means the real heat tax is likely higher than what we report.
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

MONTHS_FR = {
    1:"Jan", 2:"Fév", 3:"Mar", 4:"Avr",
    5:"Mai", 6:"Jui", 7:"Jul", 8:"Aoû",
    9:"Sep", 10:"Oct", 11:"Nov", 12:"Déc"
}

# ── Wage config ───────────────────────────────────────────────────────────────
# Source: ILO ILOSTAT EAR_INEE_CUR_NB_A, Mauritania 2022
# SMIG = 3,000 MRU/month
# Derived: 3,000 / 26 working days / 8 hours = 14.42 MRU/hour
SMIG_MONTHLY       = 3_000
WORKING_DAYS       = 26
HOURS_PER_DAY      = 8
SMIG_HOURLY        = SMIG_MONTHLY / WORKING_DAYS / HOURS_PER_DAY  # 14.42 MRU/h

# Three wage scenarios — stated explicitly
# Conservative: exactly SMIG
# Midpoint: 1.4x SMIG — reasonable for Nouakchott informal sector
# Upper: 1.8x SMIG — upper bound for skilled informal workers
WAGE_SCENARIOS = {
    "conservative": SMIG_HOURLY * 1.0,
    "midpoint":     SMIG_HOURLY * 1.4,
    "upper":        SMIG_HOURLY * 1.8,
}

# ── Exposed workforce ─────────────────────────────────────────────────────────
# Outdoor/semi-outdoor informal workers in Nouakchott
# Source: INS Mauritanie + World Bank — informal = 91.1% of non-ag private sector
# Heat-exposed share (vendors + construction + transport + port): ~35–45%
# Nouakchott informal workforce estimate: ~300,000
# Exposed workers: 300,000 × 40% = 120,000 central estimate
EXPOSED_WORKERS = {
    "low":  100_000,
    "mid":  120_000,
    "high": 150_000,
}


def main():
    print("Loading work_capacity_monthly.csv...")
    df = pd.read_csv(PROCESSED_DIR / "work_capacity_monthly.csv")
    print(f"  {len(df)} rows loaded")

    # ── Average across all years by month ─────────────────────────────────────
    avg = df.groupby("month").agg(
        month_label    = ("month_label",     "first"),
        mean_temp      = ("mean_temp_c",     "mean"),
        hours_lost     = ("hours_lost",      "mean"),
        compression    = ("compression_pct", "mean"),
    ).reset_index()

    # ── Apply wage scenarios ──────────────────────────────────────────────────
    records = []
    for _, row in avg.iterrows():
        rec = {
            "month":        int(row["month"]),
            "month_label":  row["month_label"],
            "mean_temp_c":  round(row["mean_temp"], 2),
            "hours_lost":   round(row["hours_lost"], 1),
            "compression_pct": round(row["compression"], 1),
        }

        # Cost per worker per month (each wage scenario)
        for scenario, hourly_wage in WAGE_SCENARIOS.items():
            rec[f"cost_per_worker_mru_{scenario}"] = round(
                row["hours_lost"] * hourly_wage, 1
            )

        # City-wide cost per month (mid wage × each workforce size)
        mid_wage = WAGE_SCENARIOS["midpoint"]
        for size, n_workers in EXPOSED_WORKERS.items():
            rec[f"city_cost_mru_{size}"] = round(
                row["hours_lost"] * mid_wage * n_workers, 0
            )

        records.append(rec)

    result = pd.DataFrame(records)
    result.to_csv(PROCESSED_DIR / "compression_cost.csv", index=False)
    print(f"  Saved → compression_cost.csv")

    # ── Print monthly detail ──────────────────────────────────────────────────
    print(f"\n── Monthly cost per worker (MRU) ────────────────────────────")
    print(f"{'':4s}  {'°C':>5}  {'Hrs lost':>9}  {'Conservative':>13}  {'Midpoint':>9}  {'Upper':>7}")
    print(f"{'':4s}  {'─────':>5}  {'─────────':>9}  {'─────────────':>13}  {'─────────':>9}  {'───────':>7}")
    for _, row in result.iterrows():
        print(
            f"{row['month_label']:4s}  "
            f"{row['mean_temp_c']:>5.1f}  "
            f"{row['hours_lost']:>9.1f}  "
            f"{row['cost_per_worker_mru_conservative']:>13,.0f}  "
            f"{row['cost_per_worker_mru_midpoint']:>9,.0f}  "
            f"{row['cost_per_worker_mru_upper']:>7,.0f}"
        )

    # ── Annual totals ─────────────────────────────────────────────────────────
    annual_hours     = result["hours_lost"].sum()
    annual_cost_low  = result["cost_per_worker_mru_conservative"].sum()
    annual_cost_mid  = result["cost_per_worker_mru_midpoint"].sum()
    annual_cost_high = result["cost_per_worker_mru_upper"].sum()

    print(f"\n── Annual cost per worker ───────────────────────────────────")
    print(f"  Hours lost per year:     {annual_hours:,.0f}h")
    print(f"  Conservative (1.0x SMIG): {annual_cost_low:,.0f} MRU/year")
    print(f"  Midpoint    (1.4x SMIG): {annual_cost_mid:,.0f} MRU/year")
    print(f"  Upper       (1.8x SMIG): {annual_cost_high:,.0f} MRU/year")
    print(f"  As % of annual SMIG:     {annual_cost_mid / (SMIG_MONTHLY * 12) * 100:.1f}%")

    # ── City-wide annual cost ─────────────────────────────────────────────────
    print(f"\n── City-wide annual cost (midpoint wage) ────────────────────")
    for size, n_workers in EXPOSED_WORKERS.items():
        total = result[f"city_cost_mru_{size}"].sum()
        print(
            f"  {size:8s} ({n_workers:,} workers):  "
            f"{total/1_000_000:,.1f}M MRU/year  "
            f"≈ ${total/36/1_000_000:,.1f}M USD/year"
        )

    print(f"\n── The heat tax in plain language ───────────────────────────")
    pct_of_smig = annual_cost_mid / (SMIG_MONTHLY * 12) * 100
    print(f"  The average outdoor worker in Nouakchott loses")
    print(f"  {annual_cost_mid:,.0f} MRU per year to heat — {pct_of_smig:.0f}% of their annual SMIG.")
    print(f"  That is {annual_hours:.0f} hours of potential income, gone.")


if __name__ == "__main__":
    main()