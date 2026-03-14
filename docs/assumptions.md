# Assumptions Log
Every assumption stated explicitly. This is the project's shield.

Format:
ASSUMPTION: [what was assumed]
REASON: [why]
ALTERNATIVE: [what else, and how it changes results]
SOURCE: [where it comes from]
STATUS: [VERIFIED | PLACEHOLDER | UPDATED]

---

## Temperature

ASSUMPTION: Primary heat threshold set at 38°C dry bulb.
REASON: Conservative Nouakchott-specific proxy consistent with
observed behavioral changes. WHO and ILO cite 35°C wet bulb as
extreme danger — 38°C dry bulb is the conservative equivalent.
ALTERNATIVE: 35°C would increase hours lost by ~15%. Results
available at all thresholds in temp_monthly.csv.
SOURCE: WHO Environmental Health Criteria; ILO heat stress guidance.
STATUS: VERIFIED

---

ASSUMPTION: Analysis window is 08:00–18:00 local time (UTC+0).
REASON: Standard working hours in Mauritania.
ALTERNATIVE: 07:00–19:00 would increase hours counted.
STATUS: VERIFIED

---

## Activity Curve

ASSUMPTION: Work capacity curve from ILO/ISO standards applied
to dry bulb temperature. Moderate work intensity.
REASON: No behavioral data available for Nouakchott (Google Maps
Popular Times absent — insufficient user density). ILO/ISO is
more defensible than scraped data — peer-reviewed, internationally
standardized, fully citable.
ALTERNATIVE: Heavy intensity would show more compression.
Light intensity would show less.
SOURCE: ILO (2019) Working on a Warmer Planet. ISO 7243:2017.
STATUS: VERIFIED

---

ASSUMPTION: Moderate work intensity represents market vendors,
construction workers, and port workers.
REASON: These professions involve sustained physical activity —
standing, carrying, assembling — consistent with ISO 7243
moderate intensity classification (200–300W metabolic rate).
STATUS: VERIFIED

---

## Wages

ASSUMPTION: Base wage anchored to SMIG 3,000 MRU/month (ILO 2022).
REASON: Publicly verifiable, legally defined, citable. Using SMIG
understates the real loss — informal workers often earn more.
This makes our estimate a conservative lower bound.
SOURCE: ILO ILOSTAT EAR_INEE_CUR_NB_A dataset, Mauritania 2022.
ALTERNATIVE: INS informal sector survey data would be more precise.
STATUS: VERIFIED — verify if updated since 2022

---

ASSUMPTION: Informal worker wage multipliers:
  1.0x SMIG — conservative lower bound
  1.4x SMIG — midpoint estimate
  1.8x SMIG — upper bound
REASON: ILO and World Bank informal sector studies find informal
wages at 1.2–2.0x formal minimums in West African urban contexts.
STATUS: PLACEHOLDER — improve with INS data if available

---

## Exposed Workforce

ASSUMPTION: Heat-exposed outdoor workers in Nouakchott: 100,000–150,000
(central estimate: 120,000).
REASON: INS informal sector = 91.1% of non-agricultural private sector.
Heat-exposed share (vendors + construction + transport + port): ~40%.
SOURCE: INS Mauritanie; World Bank labor force data.
STATUS: PLACEHOLDER — verify with INS survey

---

## AC Premium

ASSUMPTION: Average commercial plot size: 120 m².
REASON: Standard small boutique size in Nouakchott commercial areas.
ALTERNATIVE: 100 m² would increase unit count by 20%.
STATUS: PLACEHOLDER — improve with field observation

---

ASSUMPTION: AC penetration rate: 1 in 3 commercial spaces.
REASON: Local knowledge — most Nouakchott commercial buildings have
AC in the owner's room or back office only. Not full coverage.
Conservative estimate.
ALTERNATIVE: 1 in 5 (conservative) to 1 in 2 (upper). All three
scenarios reported in ac_premium.csv.
STATUS: LOCAL KNOWLEDGE — stated explicitly

---

ASSUMPTION: Standard AC unit = 2.5 kW (1-ton split unit).
REASON: Most common unit size for small commercial spaces in Mauritania.
ALTERNATIVE: Larger units (5kW) would double the estimate.
STATUS: PLACEHOLDER — improve with field observation

---

ASSUMPTION: AC units run at 75% efficiency on average.
REASON: Accounts for thermostat cycling, off periods, older units.
ALTERNATIVE: 100% would increase cost by 33%.
STATUS: VERIFIED — standard engineering assumption

---

ASSUMPTION: Government buildings included in AC premium at same
penetration rate as commercial.
REASON: Same SOMELEC rate applies (5.903 MRU/kWh, tariff 9106–9136).
Government offices are heavily AC'd but not uniformly.
STATUS: VERIFIED

---

## Shadow Output

ASSUMPTION: Shadow Output is NOT a national accounts measure.
It is a scalar applied to observed temperature patterns to estimate
heat-induced compression. It does not correspond to GDP or any
official statistic.
REASON: To avoid any confusion with national accounts and stay
within defensible descriptive analysis.
STATUS: NON-NEGOTIABLE

---

## What This Analysis Does NOT Claim

- Does NOT claim heat causes lower GDP
- Does NOT predict future losses or climate change impacts
- Does NOT cover agriculture or fishing sector
- Does NOT represent all workers — outdoor/semi-outdoor only
- Work capacity curve is for moderate work intensity only
- All figures are lower bound estimates unless stated otherwise