# La Taxe Canicule — Nouakchott Heat Tax

**Nouakchott runs at 80% of its potential. Heat takes the rest.**

A data analysis measuring heat-induced economic compression in Nouakchott, Mauritania — 2019–2025.

→ **[Live site](https://mauritan.site)** · [English](https://mauritan.site/en/)

---

## The number

> 20% of Nouakchott's working capacity is lost to heat every year.
> An outdoor worker loses 730 hours — 41% of the annual minimum wage.
> The total heat tax: **2,638M MRU ≈ $73M USD / year**.

This is not a model. It is a measurement.

---

## Method

The analysis has two components:

**1. Worker income loss**
The ILO/ISO occupational heat stress curve (ILO 2019, ISO 7243:2017) applied hour by hour to six years of Open-Meteo temperature data for Nouakchott. Anchored to Mauritania's SMIG (ILO ILOSTAT, 2022). 120,000 exposed workers, central estimate.

**2. Commercial AC premium**
Commercial stock estimated from the JICA 2018 Nouakchott Urban Master Plan (Table I-14). AC penetration: 1 in 3. Electricity rate: SOMELEC INDUST/ARTISAN/COMMERCE, 5.903 MRU/kWh.

No regressions. No causality claims. Transparent arithmetic from primary sources.

---

## Key findings

| Metric | Value |
|---|---|
| Shadow output | 80.0% of potential |
| Annual compression | 20.0% |
| Worst month | **October** — 37.8% (not July) |
| Best month | January — 9.0% |
| Hours lost / worker / year | 730h |
| Cost / worker (central) | 14,742 MRU = 41% of annual SMIG |
| City income loss (central) | 1,769M MRU ≈ $49M USD |
| AC premium (central) | 869M MRU ≈ $24M USD |
| **Total heat tax** | **2,638M MRU ≈ $73M USD** |

The hardest month is October, not July. The harmattan moderates July. October has no such excuse.

---

## Data sources

| Source | Use | Status |
|---|---|---|
| [Open-Meteo Historical API](https://open-meteo.com) | Hourly temperature 2019–2025 | ✅ CC BY 4.0 |
| ILO (2019) *Working on a Warmer Planet* | Work capacity curve | ✅ Public |
| ISO 7243:2017 | Heat stress standard | ✅ |
| [JICA 2018 Nouakchott Master Plan](https://openjicareport.jica.go.jp/pdf/12324729.pdf) | Commercial stock (Table I-14) | ✅ Public |
| SOMELEC Tarifs Basse Tension | Electricity rate (5.903 MRU/kWh) | ✅ |
| ILO ILOSTAT EAR_INEE_CUR_NB_A | SMIG 3,000 MRU/month (2022) | ✅ Public |
| OpenStreetMap Overpass API | Commercial buildings (lower bound) | ✅ ODbL |

---

## Project structure

```
nkc-heat-tax/
├── data/
│   ├── raw/
│   │   ├── temperature/          # Open-Meteo hourly download
│   │   └── osm/                  # OSM commercial building features
│   └── processed/
│       ├── temp_hourly.csv
│       ├── work_capacity_monthly.csv
│       ├── compression_cost.csv
│       ├── ac_premium.csv
│       └── shadow_output.csv     # Final synthesis
├── src/
│   ├── collection/
│   │   ├── 01_get_temperature.py
│   │   └── 03_get_osm_buildings.py
│   ├── analysis/
│   │   ├── 04_clean_temperature.py
│   │   ├── 05_activity_curve.py
│   │   ├── 06_compression_rate.py
│   │   ├── 07_ac_premium.py
│   │   └── 08_shadow_output.py
│   └── visualization/
│       ├── chart_style.py
│       ├── 09_chart_activity_curve.py
│       ├── 10_chart_compression.py
│       ├── 11_chart_calendar.py
│       └── 12_chart_shadow.py
├── site/                         # Static site (14 pages, FR + EN)
│   ├── index.html
│   ├── assets/charts/            # Generated chart PNGs
│   └── en/
└── docs/
    ├── assumptions.md
    └── data_sources.md
```

---

## Reproduce

```bash
git clone https://github.com/agattbechar/nkc-heat-tax.git
cd nkc-heat-tax
pip install -r requirements.txt

# Collect data
python src/collection/01_get_temperature.py
python src/collection/03_get_osm_buildings.py

# Run analysis
python src/analysis/04_clean_temperature.py
python src/analysis/05_activity_curve.py
python src/analysis/06_compression_rate.py
python src/analysis/07_ac_premium.py
python src/analysis/08_shadow_output.py

# Generate charts
python src/visualization/09_chart_activity_curve.py
python src/visualization/10_chart_compression.py
python src/visualization/11_chart_calendar.py
python src/visualization/12_chart_shadow.py
```

All data sources are free and publicly available. Results are fully reproducible from scratch.

---

## Assumptions

All key assumptions are declared explicitly:

- **Working hours**: 08:00–18:00 (standard Mauritanian commercial hours)
- **Intensity**: Moderate (200–300W metabolic rate) — market vendors, construction, port workers
- **Wage anchor**: SMIG = 3,000 MRU/month (ILO 2022) — deliberate lower bound
- **Exposed workers**: 120,000 central estimate (INS informal sector data)
- **AC penetration**: 1 in 3 commercial spaces — local knowledge, declared explicitly
- **Commercial stock**: JICA 2018 Table I-14 — primary source, OSM as lower bound check

Full assumptions documented in `docs/assumptions.md`.

---

## Limitations

- Does not claim heat *causes* lower GDP — this is descriptive, not causal
- Does not cover agriculture or fishing
- OSM commercial stock is ~15% of true total — JICA used instead
- SMIG may have been updated since 2022
- AC penetration rate is estimated, not directly measured
- All figures are lower bounds unless stated otherwise

The real heat tax is probably higher than what we report.

---

## License

- Code: MIT
- Data derived from Open-Meteo: CC BY 4.0
- Site content: CC BY 4.0

---

## Author

**Bechar Agatt** — CS student, Nouakchott, Mauritania  
[github.com/agattbechar](https://github.com/agattbechar)

---

*"Nous n'avons rien modélisé. Nous avons observé la ville, et compté."*  
*"We didn't model anything. We watched the city, and we counted."*