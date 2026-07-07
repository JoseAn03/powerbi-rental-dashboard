# 🚗 Rental Operations Dashboard - Power BI

Dashboard interactivo de operaciones de alquiler de vehículos para **Enterprise Holdings** (Alamo, Enterprise, National) + **Grupo ANC** en el Aeropuerto Internacional Juan Santamaría (SJO), Costa Rica.

---

## 📁 Estructura del proyecto

```
powerbi-rental-dashboard/
├── datasets/          ← CSVs listos para Power BI
│   ├── fact_reservations.csv      ← 4,642 reservas (3 meses)
│   ├── fact_flights.csv           ← 2,023 vuelos SJO
│   ├── dim_brands.csv             ← Marcas (Alamo, Enterprise, etc.)
│   ├── dim_customers.csv          ← 200 clientes
│   ├── dim_vehicle_categories.csv ← Categorías de vehículos
│   ├── dim_agencies.csv           ← Canales de reserva
│   ├── dim_airlines.csv           ← Aerolíneas
│   └── dim_calendar.csv           ← Tabla calendario
├── sql/
│   └── queries_powerbi.sql ← Consultas SQL optimizadas
├── dax/
│   └── measures.dax        ← 30+ medidas DAX
├── docs/
│   └── (próximamente: reporte PDF)
└── generar_datos.py     ← Script generador de datos
```

---

## 📐 Modelo de datos (Star Schema)

```
┌──────────────────┐
│   dim_calendar   │◄──────┐
│   (date)         │       │
└──────────────────┘       │
                           │
┌──────────────────┐       │  ┌────────────────────┐
│   dim_brands     │◄──────┼──│  fact_reservations  │
│   (brand_id)     │       │  │  (brand_id)         │
└──────────────────┘       │  │  (customer_id)      │
                           │  │  (category_id)      │
┌──────────────────┐       │  │  (agency_id)       │
│   dim_customers  │◄──────┼──│  (pickup_datetime)  │
│   (customer_id)  │       │  │  (return_datetime)  │
└──────────────────┘       │  │  status (activa,    │
                           │  │   completada,       │
┌──────────────────┐       │  │   no_show,          │
│ dim_vehicle_cat  │◄──────┼──│   cancelada)        │
│  (category_id)   │       │  └────────────────────┘
└──────────────────┘       │
                           │  ┌────────────────────┐
┌──────────────────┐       │  │   fact_flights     │
│   dim_agencies   │◄──────┼──│  (arrival_date)    │
│   (agency_id)    │       │  │  (airline_id)      │
└──────────────────┘       │  └────────────────────┘
                           │
┌──────────────────┐       │
│   dim_airlines   │◄──────┘
│   (airline_id)   │
└──────────────────┘
```

---

## 📊 Páginas del Dashboard

### Página 1: Executive Summary
| Visual | Medida | Tipo |
|--------|--------|------|
| KPI Cards | Revenue, Reservas, No-Show %, Avg Ticket | Tarjetas |
| Revenue Trend | Revenue Total por día | Línea |
| No-Show Rate | No Show % por día | Línea + Meta |
| Brand Mix | Reservas por marca | Donut |
| Daily Volume | Reservas por hora del día | Barra |

### Página 2: Operations Deep Dive
| Visual | Medida | Tipo |
|--------|--------|------|
| Game Plan Table | Reservas activas del día | Tabla |
| Hourly Heatmap | Reservas por hora/día | Heatmap |
| Vehicle Mix | Categorías de vehículos | Barra apilada |
| Agency Performance | Revenue por agencia | Barra horizontal |

### Página 3: No-Show Analysis
| Visual | Medida | Tipo |
|--------|--------|------|
| No-Show Trend | No-Show % por semana | Línea |
| No-Show by Brand | No-Show % por marca | Columna |
| No-Show by Agency | No-Show % por canal | Barra |
| Loss Impact | Pérdida estimada por No-Show | Tarjeta |
| Correlation | No-Show vs Ticket Promedio | Scatter |

### Página 4: Group Comparison (Enterprise vs Grupo ANC)
| Visual | Medida | Tipo |
|--------|--------|------|
| Revenue Comparison | Revenue por grupo | Columna agrupada |
| No-Show Comparison | No-Show % por grupo | Columna |
| Rental Duration | Días promedio por grupo | Barra |
| Market Share | Reservas por marca dentro grupo | Donut |

### Página 5: SJO Flight Traffic
| Visual | Medida | Tipo |
|--------|--------|------|
| Daily Flights | Vuelos por día | Línea |
| International vs Domestic | Proporción | Donut |
| Delay Rate | % Retrasos por aerolínea | Barra |
| Passenger Volume | Pasajeros estimados vs reales | Línea doble |

---

## 🛠️ Cómo cargar en Power BI

1. **Abrí Power BI Desktop**
2. **Get Data → Text/CSV**
3. Seleccioná todos los archivos CSV de la carpeta `datasets/`
4. En **Model View**, conectá las relaciones:

| Desde | Hacia | Columna |
|-------|-------|---------|
| fact_reservations | dim_brands | brand_id |
| fact_reservations | dim_customers | customer_id |
| fact_reservations | dim_vehicle_categories | category_id |
| fact_reservations | dim_agencies | agency_id |
| fact_reservations | dim_calendar | pickup_datetime ↔ date |
| fact_flights | dim_calendar | arrival_datetime ↔ date |
| fact_flights | dim_airlines | airline_id |

5. **Creá una tabla "Measures"** y pegá las medidas DAX de `dax/measures.dax`
6. Empezá a armar las visualizaciones

---

## 🎯 KPIs Clave a Monitorear

| KPI | Fórmula | Target |
|-----|---------|--------|
| No-Show Rate | No-Shows / Total Reservas | < 10% |
| Revenue Diario | Promedio revenue/día | Incremental |
| Ticket Promedio | Revenue / Reservas | $50+ |
| Ocupación Diaria | Reservas/día | 40+ |
| Duración Promedio | Días alquiler promedio | 2.5+ días |
| % Retrasos Vuelos | Vuelos retrasados / Total | < 20% |

---

## 💡 Próximos pasos

- [ ] Cargar datos reales de Enterprise + Grupo ANC
- [ ] Agregar datos de ejemplo de otras empresas
- [ ] Publicar en Power BI Service
- [ ] Configurar refresh automático
- [ ] Agregar página de predicción No-Show (ML)
