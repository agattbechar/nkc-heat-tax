# La Taxe Canicule — Project State
> Last updated: 2026-03-08
> Read this file first. It tells you everything.

---

## What This Project Is

A descriptive measurement of heat-induced economic compression in Nouakchott.
No causality claims. No p-values. Observable data, transparent arithmetic, public code.

**The one-line methodology:**
"We applied the ILO/ISO work capacity curve to six years of hourly temperature
data for Nouakchott. The standards did the work. We just ran the numbers."

**The output:** One number. "Nouakchott runs at 80.0% of potential."

**Three professions. Three lenses:**
| Profession | Evidence type |
|---|---|
| Market vendors (Marché Capitale, Marché 5ème) | Behavioral — foot traffic vs. temperature |
| Construction workers (maçons, journaliers) | Physical — body can't work at 45°C |
| Commercial shops (downtown, Avenue Nasser) | Financial — real money spent on cooling |

**Four calculations:**
1. Activity Curve — ILO/ISO work capacity curve applied to hourly temperature data ✅
2. Compression Rate — effective work capacity by month vs. potential ✅
3. AC Premium — total cooling cost paid by commercial Nouakchott per year ⏳
4. Shadow Output — "Nouakchott runs at X% of potential" ⬜

---

## Project Structure
```
nkc-heat-tax/
├── STATE.md                             ← YOU ARE HERE
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── temperature/                 ✅ 2019–2025 hourly
│   │   ├── popular_times/               ⛔ abandoned — see decision log
│   │   ├── osm/                         ✅ 168 features, 267,658 m² usable
│   │   └── somelec/                     ✅ 5.903 MRU/kWh
│   ├── processed/
│   │   ├── temp_hourly.csv              ✅
│   │   ├── temp_monthly.csv             ✅
│   │   ├── work_capacity_hourly.csv     ✅
│   │   ├── work_capacity_monthly.csv    ✅
│   │   ├── compression_cost.csv         ✅
│   │   └── ac_premium.csv               ⏳ floor space being refined
│   └── external/
│       ├── smig_mauritania.md           ✅
│       └── jica_land_use.md             ⏳ need Table I-14 values
├── src/
│   ├── collection/
│   │   ├── 01_get_temperature.py        ✅
│   │   ├── 02_get_popular_times.py      ⛔ abandoned
│   │   └── 03_get_osm_buildings.py      ✅
│   └── analysis/
│       ├── 04_clean_temperature.py      ✅
│       ├── 05_activity_curve.py         ✅
│       ├── 06_compression_rate.py       ✅
│       ├── 07_ac_premium.py             ⏳ floor space being refined
│       └── 08_shadow_output.py          ⬜
├── site/                                ⬜
└── docs/
    ├── assumptions.md
    └── data_sources.md
```

---

## Decision Log

### Popular Times — Abandoned
**What we tried:**
1. Google Maps UI — "not enough data" for Nouakchott locations
2. `populartimes` Python library — pip network blocked
3. Google Places API (legacy) — activation failed in Google Console (UI bug)
4. SerpAPI google_maps engine — `popular_times` field absent from all responses

**Root cause:** Nouakchott has insufficient Google Maps user density to
generate Popular Times data. Data availability issue, not technical.

**What we use instead:** ILO/ISO international heat stress standards.
Stronger than behavioral data — peer-reviewed, internationally standardized,
fully citable. Cannot be challenged on data quality grounds.

**Citations:**
- ILO (2019). Working on a Warmer Planet. Geneva: ILO.
- ISO 7243:2017. Ergonomics of the thermal environment.
- ISO 7933:2004. Ergonomics — Analytical determination of heat stress.

---

### AC Premium Floor Space — In Progress
**Problem:** OSM captures only ~40% of true commercial stock in Nouakchott.
267,658 m² usable after filtering — likely undercount by 2–3x.

**Sources being triangulated:**
1. OSM (confirmed): 267,658 m² — verified lower bound
2. Population-based: 1,550,000 × 0.4 m²/capita = 620,000 m²
3. JICA Master Plan 2018 Table I-14 — awaiting manual extraction
   URL: https://openjicareport.jica.go.jp/pdf/12324729.pdf
   What to find: "Commerce/Services" row, area in hectares

**Status:** Will update 07_ac_premium.py once JICA number is extracted.

---

## Current Status — All analysis COMPLETE ✅

| Script | Status |
|---|---|
| 04_clean_temperature.py | ✅ |
| 05_activity_curve.py | ✅ |
| 06_compression_rate.py | ✅ |
| 07_ac_premium.py | ✅ |
| 08_shadow_output.py | ✅ |

## Final Numbers — CONFIRMED
| Metric | Value |
|---|---|
| Shadow output | 80.0% of potential |
| Annual compression | 20.0% |
| Worst month | October — 37.8% loss |
| Hours lost/worker/year | 730h |
| Cost/worker/year (mid) | 14,742 MRU = 41% of SMIG |
| City income loss | 1,769M MRU ≈ $49M USD/year |
| AC premium (stated) | 869M MRU ≈ $24M USD/year |
| Total heat tax | 2,638M MRU ≈ $73M USD/year |

## Next Phase — Visualization + Site