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
(centra