"""
src/collection/01_get_temperature.py
Pull hourly temperature data for Nouakchott from Open-Meteo.
No API key. No account. Free.

Output: data/raw/temperature/nouakchott_hourly_YYYY.csv (one per year)
        data/raw/temperature/nouakchott_hourly_all.csv  (combined)
"""

import requests
import pandas as pd
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
LAT   = 18.0858
LON   = -15.9785
YEARS = range(2019, 2026)  # 2019–2025 inclusive

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "temperature"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── Fetch ─────────────────────────────────────────────────────────────────────
def fetch_year(year: int) -> pd.DataFrame:
    r = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude":   LAT,
            "longitude":  LON,
            "start_date": f"{year}-01-01",
            "end_date":   f"{year}-12-31",
            "hourly":     "temperature_2m",
            "timezone":   "Africa/Nouakchott",
        },
        timeout=30,
    )
    r.raise_for_status()
    payload = r.json()

    df = pd.DataFrame({
        "datetime": pd.to_datetime(payload["hourly"]["time"]),
        "temp_c":   payload["hourly"]["temperature_2m"],
    })
    df["year"]  = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["hour"]  = df["datetime"].dt.hour
    return df


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    all_years = []

    for year in YEARS:
        print(f"Fetching {year}...", end=" ", flush=True)
        df = fetch_year(year)
        path = OUTPUT_DIR / f"nouakchott_hourly_{year}.csv"
        df.to_csv(path, index=False)
        print(f"{len(df):,} rows → {path.name}")
        all_years.append(df)

    combined = pd.concat(all_years, ignore_index=True)
    combined.to_csv(OUTPUT_DIR / "nouakchott_hourly_all.csv", index=False)

    print(f"\nCombined → nouakchott_hourly_all.csv")
    print(f"Rows   : {len(combined):,}")
    print(f"Range  : {combined['datetime'].min()} → {combined['datetime'].max()}")
    print(f"Temp   : {combined['temp_c'].min():.1f}°C min  /  {combined['temp_c'].max():.1f}°C max")


if __name__ == "__main__":
    main()