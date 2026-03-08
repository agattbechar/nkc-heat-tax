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

**The output:** One number. "Nouakchott runs at X% of potential."

**Three professions. Three lenses:**
| Profession | Evidence type |
|---|---|
| Market vendors (Marché Capitale, Marché 5ème) | Behavioral — foot traffic vs. temperature |
| Construction workers (maçons, journaliers) | Physical — body can't work at 45°C |
| Commercial shops (downtown, Avenue Nasser) | Financial — real money spent on cooling |

**Four calculations:**
1. Activity Curve — ILO/ISO work capacity curve applied to hourly temperature data
2. Compression Rate — effective work capacity by month vs. potential
3. AC Premium — total cooling cost paid by commercial Nouakchott per year
4. Shadow Output — "Nouakchott runs at X% of potential"

---

## Project Structure
```
nkc-heat-tax/
├── STATE.md                             ← YOU ARE HERE
├── README.md                            ← Full methodology and build plan
├── requirements.txt                     ← Python dependencies
├── data/
│   ├── raw/
│   │   ├── temperature/                 ← Open-Meteo hourly CSVs ✅
│   │   ├── popular_times/               ← Abandoned — see decision log below
│   │   ├── osm/                         ← OpenStreetMap building footprints ✅
│   │   └── somelec/                     ← Electricity tariff ✅
│   ├── processed/                       ← Output of analysis scripts
│   └── external/
│       └── smig_mauritania.md           ← SMIG + SOMELEC reference ✅
├── src/
│   ├── collection/                      ← Raw data scripts
│   │   ├── 01_get_temperature.py        ← ✅ done
│   │   ├── 02_get_popular_times.py      ← ⛔ abandoned (see decision log)
│   │   └── 03_get_osm_buildings.py      ← ✅ done
│   └── analysis/                        ← Processing scripts
│       ├── 04_clean_temperature.py      ← ✅ done
│       ├── 05_activity_curve.py         ← ⏳ next
│       ├── 06_compression_rate.py       ← ⬜ not started
│       ├── 07_ac_premium.py             ← ⬜ not started
│       └── 08_shadow_output.py          ← ⬜ not started
├── site/                                ← Published website (mirrors mauritan.site)
└── docs/
    ├── assumptions.md                   ← Every assumption logged
    └── data_sources.md                  ← Every source with status
```

---

## Decision Log

### Popular Times — Abandoned
**What we tried:**
1. Google Maps UI — "not enough data" for all Nouakchott locations
2. `populartimes` Python library — could not install (pip network blocked)
3. Google Places API (legacy) — API activation failed in Google Console (UI bug)
4. SerpAPI google_maps engine — API calls succeeded but `popular_times` field
   absent from all responses for Nouakchott locations

**Why it failed:**
Popular Times requires sufficient Google Maps user check-in density.
Nouakchott does not have that density. This is a data availability issue,
not a technical one. No workaround exists without primary field data.

**What we use instead:**
ILO/ISO international heat stress standards — a stronger, more defensible
foundation than behavioral scraping data.

**Citations:**
- ILO "Working on a Warmer Planet" (2019) — work capacity reduction by temperature
- ISO 7243 — occupational heat stress standard, work intensity classifications
- ISO 7933 — predicted heat strain model

**Why this is better:**
A physiologically grounded, peer-reviewed, internationally standardized curve
is more defensible than scraped foot traffic data. The methodology is citable,
reproducible, and cannot be challenged on data quality grounds.

---

## Current Status

### ✅ DONE

**Environment**
- [x] requirements.txt created and installed
- [x] Directory structure created

**Raw Data Collection**
- [x] `src/collection/01_get_temperature.py`
      → Output: `data/raw/temperature/nouakchott_hourly_all.csv`
      → Period: 2019–2025, hourly, Nouakchott (lat 18.0858, lon -15.9785)

- [x] `src/collection/03_get_osm_buildings.py`
      → Output: `data/raw/osm/nouakchott_commercial_buildings.csv`
      → 168 features, 54 named, total floor space: 770,905 m²
      → NOTE: OSM coverage incomplete — lower bound
      → NOTE: 2 car entries + livestock market flagged for filtering

**Reference Data**
- [x] SOMELEC commercial rate: 5.903 MRU/kWh
      → Source: Tarifs_Basse_Tension.xls (official SOMELEC tariff sheet)
      → Tariff code: INDUST/ARTISAN/COMMERCE (7106–7136)

- [x] SMIG: 3,000 MRU/month (ILO 2022, new ouguiya)
      → Daily: ~115 MRU (26 working days)
      → Hourly: ~14.4 MRU (8h day)
      → Source: ILO ILOSTAT EAR_INEE_CUR_NB_A dataset
      → NOTE: 2022 data — verify if updated since

- [x] Activity curve standard identified
      → ILO "Working on a Warmer Planet" (2019)
      → ISO 7243 / ISO 7933 occupational heat stress standards
      → Work capacity curve by temperature documented in 05_activity_curve.py

### ⏳ IN PROGRESS

- [ ] `src/analysis/05_activity_curve.py`
      → Apply ILO/ISO work capacity curve to hourly temperature data
      → Output: work capacity % for every hour 2019–2025

### ⬜ NOT STARTED

**Analysis Scripts**
- [ ] `src/analysis/06_compression_rate.py`
- [ ] `src/analysis/07_ac_premium.py`
- [ ] `src/analysis/08_shadow_output.py`

**Visualization Scripts**
- [ ] `src/visualization/09_chart_activity_curve.py`
- [ ] `src/visualization/10_chart_compression.py`
- [ ] `src/visualization/11_chart_calendar.py`
- [ ] `src/visualization/12_chart_shadow.py`

**Site**
- [ ] All HTML pages
- [ ] French translation

---

## Key Numbers

| Number | Value | Source | Status |
|---|---|---|---|
| OSM commercial features | 168 | OpenStreetMap | ✅ |
| Total OSM floor space | 770,905 m² | OpenStreetMap | ✅ lower bound |
| Usable floor space (filtered) | ~400–500k m² | OSM minus outliers | ⏳ estimate |
| SMIG monthly | 3,000 MRU | ILO ILOSTAT 2022 | ✅ verify if updated |
| SMIG hourly | ~14.4 MRU | Derived | ✅ |
| SOMELEC commercial rate | 5.903 MRU/kWh | SOMELEC official | ✅ |
| Work capacity at 38°C | ~30–40% | ILO 2019 / ISO 7243 | ✅ |
| Work capacity at 42°C | ~10% | ISO 7933 | ✅ |
| Annual compression rate | 20.0% | ILO/ISO curve + Open-Meteo 2019–2025 | ✅ |
| Shadow output | 80.0% of potential | ILO/ISO curve + Open-Meteo 2019–2025 | ✅ |
| Worst month | October (37.8% loss) | ILO/ISO curve | ✅ |

---

## Assumptions In Use

Full log: `docs/assumptions.md`

Critical ones:
- Activity curve: ILO/ISO work capacity by temperature (not behavioral data)
- Work intensity: moderate (representative of market vendors + construction)
- Temperature metric: dry bulb (conservative — wet bulb would show more stress)
- Wage anchor: SMIG lower bound (real informal wages likely higher)
- OSM floor space: lower bound (coverage incomplete)
- Shadow Output ≠ GDP — scalar on observed temperature patterns only

---

## Next Action

Build `src/analysis/05_activity_curve.py`:
- Apply ILO/ISO work capacity curve to `data/processed/temp_hourly.csv`
- Output: hourly work capacity % for 2019–2025
- This feeds directly into compression rate and shadow output calculations

---

## What This Analysis Does NOT Claim

- Does NOT claim heat causes lower GDP
- Does NOT predict future losses
- Does NOT cover agriculture or fishing
- Does NOT represent all workers — outdoor/semi-outdoor informal sector only
- All figures are lower bound estimates unless stated otherwise
- Work capacity curve applied is for moderate work intensity only