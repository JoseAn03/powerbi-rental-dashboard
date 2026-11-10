# Rental Operations Dashboard — Car Rental Analytics (Synthetic Data)

Interactive dashboard analyzing a full year of car-rental operations at an international airport: **49,892 reservations** across 3 brands, 7 vehicle classes and 4 booking channels.

**Live demo:** open `index.html` in this repo (GitHub Pages) — a web version of the case, built with Chart.js from the same dataset. A native **Power BI** version (star schema + 30+ DAX measures) is in progress, following the build plan in this project.

## Key findings
- **Overall no-show rate: 10.8%** (excluding cancellations).
- The **Web channel has the highest no-show rate (13.7%)**; walk-in (counter) is the lowest (6.1%).
- **Prepaid reservations no-show far less: 7.1% vs 13.4%** for pay-at-counter.
- Pickups concentrate between **9:00 and 13:00 (53.9%)**, following flight arrivals; peak hour 11:00.
- **SUVs generate 39.8% of revenue**; December–April (high season) concentrates 65% of annual revenue.

## About the data
100% **synthetic data** generated with Python (fixed seed, fully reproducible) — no real customer or company data. The dataset follows a star schema: one fact table (reservations) plus calendar, brand, agency, vehicle-class and channel dimensions, designed to mirror real rental-operation patterns (seasonality, channel behavior, lead time, prepaid effects).

## Stack
Python (data generation) · Star schema modeling · Power BI / DAX (in progress) · Chart.js (web demo)

---
*Portfolio project by José Andrés Sequeira Hernández — Data Analyst (Python · SQL · Power BI · automation & applied AI). Companion case: [El costo invisible del no-show](https://github.com/JoseAn03/mini-caso-noshow).*
