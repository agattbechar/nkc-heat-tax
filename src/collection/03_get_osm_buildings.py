"""
src/collection/03_get_osm_buildings.py

Pull commercial building footprints for Nouakchott from OpenStreetMap
via the Overpass API. No account needed. Free.

What we're after:
  - Commercial buildings (shops, markets, offices)
  - Their approximate floor area (derived from footprint polygon)
  - Used in 07_ac_premium.py to estimate total cooling load

Output: data/raw/osm/nouakchott_commercial_buildings.geojson
        data/raw/osm/nouakchott_commercial_summary.csv
"""

import requests
import json
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "osm"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Nouakchott bounding box ───────────────────────────────────────────────────
# south, west, north, east
BBOX = "17.9500,-16.0800,18.1800,-15.8900"

# ── Overpass query ────────────────────────────────────────────────────────────
# Fetch all ways tagged as commercial buildings or shops
QUERY = f"""
[out:json][timeout:60];
(
  way["building"="commercial"]({BBOX});
  way["building"="retail"]({BBOX});
  way["building"="supermarket"]({BBOX});
  way["shop"]({BBOX});
  way["amenity"="marketplace"]({BBOX});
);
out body;
>;
out skel qt;
"""

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


# ── Fetch ─────────────────────────────────────────────────────────────────────
def fetch_osm() -> dict:
    print("Querying Overpass API...")
    r = requests.post(OVERPASS_URL, data={"data": QUERY}, timeout=90)
    r.raise_for_status()
    return r.json()


# ── Parse nodes and ways ──────────────────────────────────────────────────────
def parse(data: dict) -> pd.DataFrame:
    # Build node lookup: id → (lat, lon)
    nodes = {}
    for el in data["elements"]:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lat"], el["lon"])

    records = []
    for el in data["elements"]:
        if el["type"] != "way":
            continue

        tags = el.get("tags", {})
        coords = [nodes[n] for n in el.get("nodes", []) if n in nodes]

        if len(coords) < 3:
            continue

        # Rough area estimate using bounding box (good enough for our purposes)
        lats = [c[0] for c in coords]
        lons = [c[1] for c in coords]
        lat_range = max(lats) - min(lats)
        lon_range = max(lons) - min(lons)

        # Convert degrees to meters (approximate at Nouakchott latitude ~18°N)
        # 1° lat ≈ 111,000m   |   1° lon ≈ 111,000 × cos(18°) ≈ 105,600m
        height_m = lat_range * 111_000
        width_m  = lon_range * 105_600
        area_m2  = round(height_m * width_m, 1)

        records.append({
            "osm_id":       el["id"],
            "name":         tags.get("name", ""),
            "building":     tags.get("building", ""),
            "shop":         tags.get("shop", ""),
            "amenity":      tags.get("amenity", ""),
            "centroid_lat": round(sum(lats) / len(lats), 6),
            "centroid_lon": round(sum(lons) / len(lons), 6),
            "area_m2":      area_m2,
        })

    return pd.DataFrame(records)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    raw = fetch_osm()

    # Save raw GeoJSON
    raw_path = OUTPUT_DIR / "nouakchott_commercial_raw.json"
    with open(raw_path, "w") as f:
        json.dump(raw, f)
    print(f"Raw response saved → {raw_path.name}")

    # Parse to DataFrame
    df = parse(raw)
    print(f"Parsed {len(df)} commercial features")

    if df.empty:
        print("No features found — check bounding box or tags.")
        return

    # Save CSV
    csv_path = OUTPUT_DIR / "nouakchott_commercial_buildings.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved → {csv_path.name}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n── Summary ──────────────────────────────────────────────────")
    print(f"  Total features:       {len(df)}")
    print(f"  With area estimate:   {(df['area_m2'] > 0).sum()}")
    print(f"  Median area:          {df[df['area_m2'] > 0]['area_m2'].median():.0f} m²")
    print(f"  Total floor space:    {df['area_m2'].sum():,.0f} m²")
    print(f"  Named locations:      {(df['name'] != '').sum()}")

    print(f"\n── Top 10 largest by area ───────────────────────────────────")
    top = df[df['area_m2'] > 0].nlargest(10, "area_m2")[["name","building","shop","area_m2"]]
    print(top.to_string(index=False))

    print(f"\n── Building type breakdown ──────────────────────────────────")
    print(df["building"].value_counts().to_string())


if __name__ == "__main__":
    main()
    