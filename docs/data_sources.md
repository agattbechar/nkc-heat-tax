# Data Sources
Every number's origin. Updated as data is collected.

---

## 1. Temperature Data
Source: Open-Meteo Historical Weather API
URL: https://open-meteo.com/en/docs/historical-weather-api
Variables: temperature_2m (hourly, 2m above ground)
Location: Nouakchott — lat 18.0858, lon -15.9785
Period: 2019-01-01 to 2025-12-31
Timezone: Africa/Nouakchott (UTC+0)
License: CC BY 4.0
Script: src/collection/01_get_temperature.py
Status: ✅ collected

---

## 2. Activity / Work Capacity Curve
Source 1: ILO (2019). Working on a Warmer Planet.
          The impact of heat stress on labour productivity and decent work.
          Geneva: International Labour Organization.
URL: https://www.ilo.org/wcmsp5/groups/public/---dgreports/---dcomm/
     ---publ/documents/publication/wcms_711919.pdf

Source 2: ISO 7243:2017. Ergonomics of the thermal environment —
          Assessment of heat stress using the WBGT index.
          Geneva: International Organization for Standardization.

Source 3: ISO 7933:2004. Ergonomics of the thermal environment —
          Analytical determination and interpretation of heat stress
          using calculation of the predicted heat strain.

What was used: Work capacity reduction by temperature at moderate
work intensity (200–300W metabolic rate).
Status: ✅ verified and applied in 05_activity_curve.py

---

## 3. Popular Times (Abandoned)
Attempted sources:
  - Google Maps UI — insufficient data for Nouakchott
  - populartimes Python library — pip blocked
  - Google Places API legacy — activation failed
  - SerpAPI google_maps — popular_times field absent
Reason abandoned: Nouakchott has insufficient Google Maps user
density to generate Popular Times data.
Status: ⛔ abandoned — replaced by ILO/ISO standards

---

## 4. OSM Commercial Buildings
Source: OpenStreetMap via Overpass API
URL: https://overpass-api.de/api/interpreter
Query: commercial + retail + shop + marketplace tags
Bounding box: Nouakchott (17.95, -16.08, 18.18, -15.89)
License: ODbL
Script: src/collection/03_get_osm_buildings.py
Output: 168 features, 267,658 m² usable (after filtering outliers)
Note: Lower bound — OSM coverage incomplete (~15% of true stock)
Status: ✅ collected — used as lower bound reference only

---

## 5. Commercial Floor Space (Primary)
Source: JICA (2018). Nouakchott City Urban Master Plan.
        Table I-14: Composition of Existing and Proposed Land Use.
URL: https://openjicareport.jica.go.jp/pdf/12324729.pdf
What was extracted:
  Commercial land: 952 ha
  Mixed use land: 1,270 ha
  Government/public: 204 ha
Derived estimate: 94,296 total commercial spaces
AC units (1 in 3): 31,432
Status: ✅ extracted manually from PDF

---

## 6. SOMELEC Electricity Tariff
Source: SOMELEC (Société Mauritanienne d'Electricité)
File: Tarifs_Basse_Tension.xls (official tariff sheet)
Tariff code: INDUST/ARTISAN/COMMERCE (7106–7136)
Rate: 5.903 MRU/kWh
Status: ✅ verified from official file

---

## 7. Minimum Wage (SMIG)
Source: ILO ILOSTAT
Dataset: EAR_INEE_CUR_NB_A (Monthly minimum wages by currency)
Country: Mauritania
Year: 2022 (latest available)
Value: 3,000 MRU/month
Type: Rate of the SMIG when SMIG/SMAG system
Currency: MRT - Ouguiya (MRU) — new ouguiya post-2018 redenomination
Derived: 14.42 MRU/hour (÷ 26 days ÷ 8 hours)
Note: 2022 data — verify if updated since
Status: ✅ verified — check for 2023/2024 update

---

## 8. Nouakchott Population
Source: World Bank / UN estimates
Value: ~1,550,000 (2024)
Used for: Population-based floor space cross-check
Status: ✅ reference only

---

## Citation Format (for site)
Temperature: Open-Meteo Historical API, CC BY 4.0
Work capacity: ILO (2019) Working on a Warmer Planet; ISO 7243:2017
Land use: JICA (2018) Nouakchott Urban Master Plan, Table I-14
Electricity: SOMELEC Tarifs Basse Tension (official tariff sheet)
Minimum wage: ILO ILOSTAT, Mauritania SMIG 2022
Buildings: OpenStreetMap contributors, ODbL