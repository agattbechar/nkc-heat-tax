"""
src/collection/02_get_popular_times.py

Pull Popular Times data for Nouakchott locations via SerpAPI.
Free tier: 100 searches/month — more than enough.

Output: data/raw/popular_times/activity_by_hour.csv
        data/raw/popular_times/raw_responses.json
"""

import json
import requests
import pandas as pd
from pathlib import Path

API_KEY = ""    # Your Serp API Key here 

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "popular_times"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOCATIONS = [
    {
        "name":  "marche_capitale",
        "query": "marche capitale nouakchott mauritanie",
    },
    {
        "name":  "marche_cinquieme",
        "query": "marche cinquieme nouakchott",
    },
    {
        "name":  "avenue_nasser",
        "query": "ave abdel nasser nouakchott",
    },
]


# ── Fetch search results ──────────────────────────────────────────────────────
def fetch_location(query: str) -> dict:
    r = requests.get(
        "https://serpapi.com/search",
        params={
            "engine":  "google_maps",
            "q":       query,
            "api_key": API_KEY,
            "hl":      "en",
            "gl":      "mr",
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


# ── Fetch place details ───────────────────────────────────────────────────────
def get_place_details(data_id: str, place_id: str, query: str) -> dict:
    r = requests.get(
        "https://serpapi.com/search",
        params={
            "engine":   "google_maps",
            "q":        query,
            "place_id": place_id,
            "api_key":  API_KEY,
            "hl":       "en",
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


# ── Parse popular_times ───────────────────────────────────────────────────────
def parse(location_name: str, result: dict) -> pd.DataFrame:
    popular_times = result.get("popular_times", [])

    if not popular_times:
        print(f"  WARNING: No popular_times for {location_name}")
        print(f"  Available keys: {list(result.keys())}")
        return pd.DataFrame()

    rows = []
    for day_data in popular_times:
        day_name = day_data.get("day", "")
        for hour_data in day_data.get("popular_times_by_hour", []):
            rows.append({
                "location":       location_name,
                "day":            day_name,
                "hour":           hour_data.get("hour", 0),
                "activity_index": hour_data.get("busyness_score", 0),
            })
    return pd.DataFrame(rows)


# ── Summarize ─────────────────────────────────────────────────────────────────
def summarize(df: pd.DataFrame):
    print(f"\n── Effective workday (activity > 50% of peak, 08–18) ────────")
    for (loc, day), g in df.groupby(["location", "day"]):
        working = g[(g["hour"] >= 8) & (g["hour"] < 18)]
        if working.empty or working["activity_index"].max() == 0:
            continue
        peak      = working["activity_index"].max()
        effective = int((working["activity_index"] >= peak * 0.5).sum())
        print(f"  {loc:25s} {day:12s} → {effective}h  (peak={peak})")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    all_raw = {}
    all_dfs = []

    print("Fetching via SerpAPI...\n")

    for loc in LOCATIONS:
        print(f"  Searching: {loc['query']}...", end=" ", flush=True)

        # Step 1 — search to get data_id
        search_result = fetch_location(loc["query"])
        local_results = search_result.get("local_results", [])

        if not local_results:
            print(f"✗ — no results found")
            continue

        top     = local_results[0]
        data_id = top.get("data_id", "")
        print(f"found: {top.get('title','')} (data_id: {data_id[:30]}...)")

        top     = local_results[0]
        data_id = top.get("data_id", "")
        place_id = top.get("place_id", "")
        print(f"found: {top.get('title','')} | place_id: {place_id[:20]}...")

        # Step 2
        print(f"  Fetching details...", end=" ", flush=True)
        try:
            details = get_place_details(data_id, place_id, loc["query"])
            # SerpAPI returns either place_results or local_results
            if "place_results" in details:
                place_result = details["place_results"]
            elif "local_results" in details:
                place_result = details["local_results"][0]
            else:
                place_result = details
            all_raw[loc["name"]] = place_result
            print("✓")
            print(f"  Keys in place_result: {list(place_result.keys())}")

            df = parse(loc["name"], place_result)
            if not df.empty:
                all_dfs.append(df)
        except Exception as e:
            print(f"✗ — {e}")
            all_raw[loc["name"]] = {}

    # Save raw
    with open(OUTPUT_DIR / "raw_responses.json", "w", encoding="utf-8") as f:
        json.dump(all_raw, f, ensure_ascii=False, indent=2)
    print(f"\nRaw saved → raw_responses.json")

    if not all_dfs:
        print("\nNo Popular Times data retrieved.")
        print("Check raw_responses.json to see what the API returned.")
        return

    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_csv(OUTPUT_DIR / "activity_by_hour.csv", index=False)
    print(f"Saved → activity_by_hour.csv  ({len(combined)} rows)")

    summarize(combined)

    # Tuesday detail
    print(f"\n── Tuesday detail ───────────────────────────────────────────")
    tuesday = combined[combined["day"] == "Tuesday"]
    for loc in combined["location"].unique():
        subset = tuesday[tuesday["location"] == loc].sort_values("hour")
        if subset.empty:
            continue
        print(f"\n  {loc}")
        for _, row in subset.iterrows():
            if 6 <= row["hour"] <= 22:
                bar = "█" * int(row["activity_index"] / 5)
                print(f"  {int(row['hour']):02d}:00  {int(row['activity_index']):>3}  {bar}")


if __name__ == "__main__":
    main()