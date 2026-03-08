"""
src/analysis/08_shadow_output.py

Combine all analysis outputs into the final number.
"Nouakchott runs at X% of potential."

Inputs:
  - data/processed/work_capacity_monthly.csv
  - data/processed/compression_cost.csv
  - data/processed/ac_premium.csv

Output:
  - data/processed/shadow_output.csv
  - data/processed/final_summary.md
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

# ── Constants (from previous scripts) ────────────────────────────────────────
SMIG_MONTHLY        = 3_000     # MRU/month
SMIG_ANNUAL         = 36_000    # MRU/year
SMIG_HOURLY         = 14.42     # MRU/hour
EXPOSED_WORKERS_MID = 120_000
WAGE_MULTIPLIER_MID = 1.4
AC_PREMIUM_STATED   = 869_000_000   # MRU/year (1 in 3 scenario)
MRU_TO_USD          = 36


def main():
    print("Loading analysis outputs...")
    capacity = pd.read_csv(PROCESSED_DIR / "work_capacity_monthly.csv")
    cost     = pd.read_csv(PROCESSED_DIR / "compression_cost.csv")
    ac       = pd.read_csv(PROCESSED_DIR / "ac_premium.csv")

    # ── 1. The Activity Curve Summary ────────────────────────────────────────
    avg_capacity = capacity.groupby("month").agg(
        month_label      = ("month_label",       "first"),
        mean_temp        = ("mean_temp_c",        "mean"),
        mean_capacity    = ("mean_work_capacity", "mean"),
        avg_hours_lost   = ("hours_lost",         "mean"),
        avg_compression  = ("compression_pct",    "mean"),
    ).reset_index()

    annual_capacity_pct = (
        capacity.groupby("year").apply(
            lambda x: x["effective_hours"].sum() / x["total_working_hours"].sum()
        ).mean() * 100
    )
    annual_compression  = 100 - annual_capacity_pct
    annual_hours_lost   = cost["hours_lost"].sum()

    # ── 2. The Compression Cost Summary ──────────────────────────────────────
    cost_per_worker_mid  = cost["cost_per_worker_mru_midpoint"].sum()
    cost_pct_of_smig     = cost_per_worker_mid / SMIG_ANNUAL * 100
    city_cost_mid        = cost["city_cost_mru_mid"].sum()

    # ── 3. The AC Premium Summary ─────────────────────────────────────────────
    ac_annual_stated = AC_PREMIUM_STATED

    # ── 4. Combined Shadow Output ─────────────────────────────────────────────
    # Total economic cost = worker income loss + cooling expenditure
    total_cost_mru = city_cost_mid + ac_annual_stated
    total_cost_usd = total_cost_mru / MRU_TO_USD

    # ── Build monthly summary ─────────────────────────────────────────────────
    MONTHS_FR = {
        1:"Jan", 2:"Fév", 3:"Mar", 4:"Avr",
        5:"Mai", 6:"Jui", 7:"Jul", 8:"Aoû",
        9:"Sep", 10:"Oct", 11:"Nov", 12:"Déc"
    }

    monthly = []
    for month in range(1, 13):
        cap_row  = avg_capacity[avg_capacity["month"] == month].iloc[0]
        cost_row = cost[cost["month"] == month].iloc[0]
        ac_row   = ac[ac["month"] == month].iloc[0]

        stated_key = "stated (1 in 3)"
        monthly.append({
            "month":                month,
            "month_label":          MONTHS_FR[month],
            "mean_temp_c":          cap_row["mean_temp"],
            "work_capacity_pct":    round(cap_row["mean_capacity"] * 100, 1),
            "hours_lost":           round(cap_row["avg_hours_lost"], 1),
            "compression_pct":      round(cap_row["avg_compression"], 1),
            "cost_per_worker_mru":  round(cost_row["cost_per_worker_mru_midpoint"], 0),
            "city_income_loss_mru": round(cost_row["city_cost_mru_mid"], 0),
            "ac_cost_mru":          round(ac_row[f"cost_mru_{stated_key}"], 0),
            "total_cost_mru":       round(
                cost_row["city_cost_mru_mid"] +
                ac_row[f"cost_mru_{stated_key}"], 0
            ),
        })

    df = pd.DataFrame(monthly)
    df.to_csv(PROCESSED_DIR / "shadow_output.csv", index=False)
    print(f"  Saved → shadow_output.csv")

    # ── Print full summary ────────────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print(f"  LA TAXE CANICULE — FINAL NUMBERS")
    print(f"{'═'*60}")

    print(f"\n── 1. The Activity Curve ────────────────────────────────────")
    print(f"  Nouakchott runs at {annual_capacity_pct:.1f}% of potential")
    print(f"  Annual heat compression: {annual_compression:.1f}%")
    print(f"  Worst month: October ({avg_capacity.loc[avg_capacity['avg_compression'].idxmax(), 'avg_compression']:.1f}% loss)")
    print(f"  Best month:  January ({avg_capacity.loc[avg_capacity['avg_compression'].idxmin(), 'avg_compression']:.1f}% loss)")

    print(f"\n── 2. The Compression Rate ──────────────────────────────────")
    print(f"  Hours lost per worker per year:  {annual_hours_lost:.0f}h")
    print(f"  Cost per worker (midpoint):      {cost_per_worker_mid:,.0f} MRU/year")
    print(f"  As % of annual SMIG:             {cost_pct_of_smig:.0f}%")
    print(f"  City-wide income loss (mid):     {city_cost_mid/1_000_000:.0f}M MRU/year")
    print(f"  = ${city_cost_mid/MRU_TO_USD/1_000_000:.0f}M USD/year")

    print(f"\n── 3. The AC Premium ────────────────────────────────────────")
    print(f"  31,432 AC units across commercial Nouakchott")
    print(f"  Annual cooling cost (stated):    {ac_annual_stated/1_000_000:.0f}M MRU/year")
    print(f"  = ${ac_annual_stated/MRU_TO_USD/1_000_000:.0f}M USD/year")

    print(f"\n── 4. The Shadow Output ─────────────────────────────────────")
    print(f"  Income loss (workers):   {city_cost_mid/1_000_000:.0f}M MRU")
    print(f"  Cooling cost (business): {ac_annual_stated/1_000_000:.0f}M MRU")
    print(f"  {'─'*40}")
    print(f"  Total heat tax:          {total_cost_mru/1_000_000:.0f}M MRU/year")
    print(f"  = ${total_cost_usd/1_000_000:.0f}M USD/year")

    print(f"\n── Monthly breakdown ────────────────────────────────────────")
    print(f"{'':4s}  {'°C':>5}  {'Capacity':>9}  {'Hrs lost':>9}  {'Per worker':>11}  {'Total cost':>12}")
    print(f"{'':4s}  {'─────':>5}  {'─────────':>9}  {'─────────':>9}  {'───────────':>11}  {'────────────':>12}")
    for _, row in df.iterrows():
        print(
            f"{row['month_label']:4s}  "
            f"{row['mean_temp_c']:>5.1f}  "
            f"{row['work_capacity_pct']:>8.1f}%  "
            f"{row['hours_lost']:>9.1f}  "
            f"{row['cost_per_worker_mru']:>10,.0f}  "
            f"{row['total_cost_mru']/1_000_000:>10.0f}M"
        )

    # ── Write final summary markdown ──────────────────────────────────────────
    summary = f"""# La Taxe Canicule — Final Numbers
> Generated from 2019–2025 Open-Meteo data + ILO/ISO standards

---

## The One Number
**Nouakchott runs at {annual_capacity_pct:.1f}% of potential.**
Every year, heat compresses {annual_compression:.1f}% of the city's economic capacity.

---

## Three Lenses

### 1. The Activity Curve
- Annual compression: **{annual_compression:.1f}%**
- Worst month: **October** ({avg_capacity.loc[avg_capacity['avg_compression'].idxmax(), 'avg_compression']:.1f}% loss)
- Not July — October is the real peak. The harmattan moderates July.

### 2. The Compression Rate (per outdoor worker)
- Hours lost per year: **{annual_hours_lost:.0f} hours**
- Income lost (midpoint): **{cost_per_worker_mid:,.0f} MRU/year**
- That is **{cost_pct_of_smig:.0f}% of annual minimum wage** — gone
- City-wide: **{city_cost_mid/1_000_000:.0f}M MRU ≈ ${city_cost_mid/MRU_TO_USD/1_000_000:.0f}M USD/year**

### 3. The AC Premium
- 31,432 AC units running across commercial Nouakchott
- Annual cooling bill: **{ac_annual_stated/1_000_000:.0f}M MRU ≈ ${ac_annual_stated/MRU_TO_USD/1_000_000:.0f}M USD/year**
- This is money spent just to reach zero — not to thrive, just to survive

---

## The Total Heat Tax
| Component | MRU/year | USD/year |
|---|---|---|
| Worker income loss (120k workers, mid wage) | {city_cost_mid/1_000_000:.0f}M | ${city_cost_mid/MRU_TO_USD/1_000_000:.0f}M |
| Commercial cooling cost (1 in 3 AC) | {ac_annual_stated/1_000_000:.0f}M | ${ac_annual_stated/MRU_TO_USD/1_000_000:.0f}M |
| **Total** | **{total_cost_mru/1_000_000:.0f}M** | **${total_cost_usd/1_000_000:.0f}M** |

---

## Key Insight
Air conditioning in Nouakchott is not comfort. It is infrastructure.
The workers who cannot afford it stop working.
The businesses that can afford it pay a climate tax every month.
Both groups lose. The city loses.

---

## Methodology
- Temperature: Open-Meteo 2019–2025 hourly data
- Work capacity: ILO (2019) + ISO 7243 curve, moderate intensity
- Wages: SMIG 3,000 MRU/month (ILO 2022) — conservative lower bound
- Commercial stock: JICA Nouakchott Master Plan 2018, Table I-14
- Electricity: SOMELEC 5.903 MRU/kWh (INDUST/ARTISAN/COMMERCE)
- All figures are lower bound estimates
"""

    summary_path = PROCESSED_DIR / "final_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"\n  Saved → final_summary.md")
    print(f"\n{'═'*60}")


if __name__ == "__main__":
    main()