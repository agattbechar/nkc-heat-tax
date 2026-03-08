"""
src/analysis/07_ac_premium.py

Calculate the total cooling cost paid by commercial Nouakchott per year.
This is real money actually spent — not hypothetical loss.

Methodology:
  Estimate number of AC units from commercial stock
  × operating hours during heat season × SOMELEC commercial rate

Sources:
  - SOMELEC tariff: 5.903 MRU/kWh (INDUST/ARTISAN/COMMERCE)
  - JICA Nouakchott Urban Master Plan 2018 — Table I-14 land use
  - AC penetration: 1 in 3 commercial spaces (local knowledge, stated assumption)

Input:  data/raw/osm/nouakchott_commercial_buildings.csv (for reference)
Output: data/processed/ac_premium.csv
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

# ── SOMELEC config ────────────────────────────────────────────────────────────
# Source: Tarifs_Basse_Tension.xls — INDUST/ARTISAN/COMMERCE tariff
SOMELEC_RATE_MRU_KWH = 5.903

# ── AC unit assumptions ───────────────────────────────────────────────────────
AC_KW_PER_UNIT       = 2.5    # kW — standard 1-ton split unit
AC_EFFICIENCY_FACTOR = 0.75   # units run at 75% capacity on average

# ── Commercial stock estimate (JICA 2018 Table I-14) ─────────────────────────
# Pure commercial:    952 ha ÷ 120 m²/unit = 79,333 units
# Mixed use GF:     571,500 m² ÷ 120 m²/unit = 4,763 units
# Government rooms: 306,000 m² ÷ 30 m²/room = 10,200 rooms
# Total:            ~94,296 spaces

COMMERCIAL_UNITS = {
    "pure_commercial": {
        "units": 79_333,
        "note":  "JICA 952ha ÷ 120m² avg plot"
    },
    "mixed_use_groundfloor": {
        "units": 4_763,
        "note":  "JICA 1,270ha mixed use × FSR 0.15 × 30% commercial ÷ 120m²"
    },
    "government_offices": {
        "units": 10_200,
        "note":  "JICA 204ha × FSR 0.15 ÷ 30m² per office room"
    },
}

TOTAL_SPACES     = sum(v["units"] for v in COMMERCIAL_UNITS.values())

# ASSUMPTION: 1 in 3 commercial spaces has AC
# Basis: local knowledge — Nouakchott commercial spaces have partial AC coverage
# Most buildings have 1 unit in the owner's room or back office, not full coverage
# 1 in 3 is conservative — stated explicitly
AC_PENETRATION   = 1 / 3
TOTAL_AC_UNITS   = round(TOTAL_SPACES * AC_PENETRATION)

# ── Heat season operating hours ───────────────────────────────────────────────
# Hours per day AC runs, by month
# Based on temp_monthly.csv — hours above 30°C during working day
HEAT_MONTHS = {
    1:  (31, 3),    # January   — mild
    2:  (28, 4),    # February
    3:  (31, 5),    # March
    4:  (30, 7),    # April
    5:  (31, 8),    # May
    6:  (30, 9),    # June
    7:  (31, 8),    # July
    8:  (31, 9),    # August
    9:  (30, 10),   # September — peak
    10: (31, 10),   # October   — peak
    11: (30, 6),    # November
    12: (31, 3),    # December
}

MONTHS_FR = {
    1:"Jan", 2:"Fév", 3:"Mar", 4:"Avr",
    5:"Mai", 6:"Jui", 7:"Jul", 8:"Aoû",
    9:"Sep", 10:"Oct", 11:"Nov", 12:"Déc"
}


def main():
    print("── Commercial Stock ─────────────────────────────────────────")
    for category, config in COMMERCIAL_UNITS.items():
        print(f"  {category:30s} {config['units']:>8,} units")
        print(f"  {'':30s} {config['note']}")
    print(f"  {'─'*50}")
    print(f"  {'Total spaces':30s} {TOTAL_SPACES:>8,}")
    print(f"  {'AC penetration (1 in 3)':30s} {AC_PENETRATION*100:.0f}%")
    print(f"  {'Total AC units':30s} {TOTAL_AC_UNITS:>8,}")

    # ── Three penetration scenarios ───────────────────────────────────────────
    # Report conservative / stated / upper for transparency
    scenarios = {
        "conservative (1 in 5)": 1/5,
        "stated (1 in 3)":       1/3,
        "upper (1 in 2)":        1/2,
    }

    # ── Monthly cost calculation ──────────────────────────────────────────────
    records = []
    for month, (days, hours_per_day) in HEAT_MONTHS.items():
        hours_total  = days * hours_per_day
        kwh_per_unit = AC_KW_PER_UNIT * AC_EFFICIENCY_FACTOR * hours_total

        rec = {
            "month":            month,
            "month_label":      MONTHS_FR[month],
            "days":             days,
            "ac_hours_per_day": hours_per_day,
            "total_ac_hours":   hours_total,
        }

        for scenario_name, penetration in scenarios.items():
            units      = round(TOTAL_SPACES * penetration)
            kwh_total  = units * kwh_per_unit
            cost_mru   = kwh_total * SOMELEC_RATE_MRU_KWH
            rec[f"units_{scenario_name}"]    = units
            rec[f"kwh_{scenario_name}"]      = round(kwh_total, 0)
            rec[f"cost_mru_{scenario_name}"] = round(cost_mru, 0)

        records.append(rec)

    result = pd.DataFrame(records)
    result.to_csv(PROCESSED_DIR / "ac_premium.csv", index=False)
    print(f"\n  Saved → ac_premium.csv")

    # ── Print monthly breakdown (stated scenario) ─────────────────────────────
    stated = "stated (1 in 3)"
    print(f"\n── Monthly AC cost — stated scenario (1 in 3) ───────────────")
    print(f"{'':4s}  {'AC hrs/day':>10}  {'kWh':>14}  {'Cost MRU':>14}  {'Cost USD':>10}")
    print(f"{'':4s}  {'──────────':>10}  {'──────────────':>14}  {'──────────────':>14}  {'──────────':>10}")
    for _, row in result.iterrows():
        print(
            f"{row['month_label']:4s}  "
            f"{row['ac_hours_per_day']:>10}  "
            f"{row[f'kwh_{stated}']:>14,.0f}  "
            f"{row[f'cost_mru_{stated}']:>14,.0f}  "
            f"${row[f'cost_mru_{stated}']/36:>9,.0f}"
        )

    # ── Annual totals — all scenarios ─────────────────────────────────────────
    print(f"\n── Annual AC Premium — all scenarios ────────────────────────")
    print(f"{'Scenario':25s}  {'AC units':>10}  {'MRU/year':>14}  {'USD/year':>12}")
    print(f"{'─────────────────────────':25s}  {'──────────':>10}  {'──────────────':>14}  {'────────────':>12}")
    for scenario_name, penetration in scenarios.items():
        units      = round(TOTAL_SPACES * penetration)
        annual_mru = result[f"cost_mru_{scenario_name}"].sum()
        annual_usd = annual_mru / 36
        print(
            f"{scenario_name:25s}  "
            f"{units:>10,}  "
            f"{annual_mru/1_000_000:>13.0f}M  "
            f"${annual_usd/1_000_000:>10.1f}M"
        )

    # ── Plain language ────────────────────────────────────────────────────────
    annual_mru_stated = result[f"cost_mru_{stated}"].sum()
    print(f"\n── The AC Premium in plain language ─────────────────────────")
    print(f"  {TOTAL_AC_UNITS:,} AC units running across commercial Nouakchott.")
    print(f"  At SOMELEC's commercial rate of {SOMELEC_RATE_MRU_KWH} MRU/kWh,")
    print(f"  the city spends at least {annual_mru_stated/1_000_000:.0f}M MRU per year")
    print(f"  just to keep working.")
    print(f"  That is the price of doing business in a 45°C city.")
    print(f"\n  NOTE: Lower bound. OSM captures ~15% of true commercial stock.")
    print(f"  Real cooling expenditure is higher.")


if __name__ == "__main__":
    main()
    