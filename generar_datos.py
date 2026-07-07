#!/usr/bin/env python3
"""
Generador de datasets sintéticos para Power BI Dashboard
Proyecto: Rental Operations Dashboard + Grupo ANC
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ─── Config ───
NUM_DAYS = 90  # 3 meses de datos
START_DATE = datetime(2026, 4, 1)
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Dimensiones ───

# 1. Marcas / Brands
brands = pd.DataFrame({
    'brand_id': [1, 2, 3, 4, 5],
    'brand_name': ['Alamo', 'Enterprise', 'National', 'Grupo ANC', 'Budget'],
    'group': ['Enterprise Holdings', 'Enterprise Holdings', 'Enterprise Holdings', 'Grupo ANC', 'Grupo ANC'],
    'priority': ['Premium', 'Standard', 'Standard', 'Premium', 'Economy']
})

# 2. Categorías de vehículos
vehicle_categories = pd.DataFrame({
    'category_id': range(1, 7),
    'category_name': ['Economy', 'Compact', 'Midsize', 'Full Size', 'SUV', 'Luxury'],
    'daily_rate': [25, 35, 45, 55, 70, 120],
    'multiplier': [1.0, 1.2, 1.4, 1.6, 2.0, 3.0]
})

# 3. Clientes
NUM_CUSTOMERS = 200
first_names = ['Carlos','Maria','Jose','Ana','Pedro','Laura','Diego','Sofia','Andres','Elena',
               'Juan','Camila','Luis','Valentina','David','Gabriela','Miguel','Isabella','Pablo','Valeria']
last_names = ['Rodriguez','Mora','Jimenez','Quesada','Araya','Castro','Vargas','Chacon','Herrera','Cruz',
              'Ramirez','Fernandez','Alfaro','Solano','Urena','Mendez','Peralta','Rojas','Campos','Aguilar']

customers = pd.DataFrame({
    'customer_id': range(1, NUM_CUSTOMERS + 1),
    'first_name': [random.choice(first_names) for _ in range(NUM_CUSTOMERS)],
    'last_name': [random.choice(last_names) for _ in range(NUM_CUSTOMERS)],
    'email': [f'cliente{i}@email.com' for i in range(1, NUM_CUSTOMERS + 1)],
    'phone': [f'+506 8{random.randint(100,9999):04d}' for _ in range(NUM_CUSTOMERS)],
    'is_vip': [random.random() < 0.08 for _ in range(NUM_CUSTOMERS)],
    'is_corporate': [random.random() < 0.25 for _ in range(NUM_CUSTOMERS)]
})

# 4. Agencias / Fuentes de reserva
agencies = pd.DataFrame({
    'agency_id': range(1, 9),
    'agency_name': ['Direct','Expedia','Booking.com','Kayak','Priceline','Travelocity','Orbitz','Corporate'],
    'is_online': [False, True, True, True, True, True, True, False],
    'commission_pct': [0, 15, 12, 10, 14, 11, 13, 5]
})

# 5. Aerolíneas (para vuelos)
airlines = pd.DataFrame({
    'airline_id': range(1, 13),
    'airline_code': ['AA','UA','DL','AV','CM','IB','KL','BA','AF','LH','AC','MX'],
    'airline_name': ['American Airlines','United Airlines','Delta Air Lines','Avianca','Copa Airlines',
                     'Iberia','KLM','British Airways','Air France','Lufthansa','Air Canada','Mexicana']
})

# 6. Estados de reserva
statuses = ['activa', 'completada', 'no_show', 'cancelada']

# ─── Tabla de Hechos: Reservas ───
print("Generando reservas...")
reservations = []
cur_id = 1

for day_offset in range(NUM_DAYS):
    date = START_DATE + timedelta(days=day_offset)
    is_weekend = date.weekday() >= 5
    
    # Más reservas en fin de semana y verano
    base_count = random.randint(50, 80) if is_weekend else random.randint(35, 60)
    if date.month in [7, 8, 12]:  # temporada alta
        base_count = int(base_count * 1.3)
    
    for _ in range(base_count):
        brand = brands.sample(1, weights=[0.30, 0.35, 0.20, 0.10, 0.05]).iloc[0]
        cat = vehicle_categories.sample(1, weights=[0.20, 0.25, 0.20, 0.15, 0.15, 0.05]).iloc[0]
        customer = customers.sample(1).iloc[0]
        agency = agencies.sample(1, weights=[0.25, 0.15, 0.12, 0.10, 0.10, 0.08, 0.08, 0.12]).iloc[0]
        
        pickup_hour = random.randint(6, 22) if not is_weekend else random.randint(7, 23)
        pickup_minute = random.choice([0, 15, 30, 45])
        pickup_time = date.replace(hour=pickup_hour, minute=pickup_minute)
        
        # Duración de renta (1-7 días)
        rental_days = random.choices([1,2,3,4,5,6,7], weights=[0.20,0.25,0.25,0.15,0.08,0.05,0.02])[0]
        return_time = pickup_time + timedelta(days=rental_days, hours=random.randint(0, 4))
        
        # Estado
        status = random.choices(
            ['activa', 'completada', 'no_show', 'cancelada'],
            weights=[0.05, 0.75, 0.12, 0.08]
        )[0]
        
        total_amount = cat['daily_rate'] * rental_days * (1 + 0.13)  # +13% impuestos
        total_amount = round(total_amount, 2)
        
        reservations.append({
            'reservation_id': cur_id,
            'brand_id': int(brand['brand_id']),
            'customer_id': int(customer['customer_id']),
            'category_id': int(cat['category_id']),
            'agency_id': int(agency['agency_id']),
            'pickup_datetime': pickup_time,
            'return_datetime': return_time,
            'rental_days': rental_days,
            'total_amount': total_amount,
            'daily_rate_applied': float(cat['daily_rate']),
            'status': status,
            'is_vip': bool(customer['is_vip']),
            'is_corporate': bool(customer['is_corporate']),
            'created_at': pickup_time - timedelta(days=random.randint(0, 30))
        })
        cur_id += 1

reservas_df = pd.DataFrame(reservations)
print(f"  → {len(reservas_df)} reservas generadas")
print(f"  → No-Shows: {len(reservas_df[reservas_df['status']=='no_show'])} ({len(reservas_df[reservas_df['status']=='no_show'])/len(reservas_df)*100:.1f}%)")

# ─── Tabla de Vuelos SJO ───
print("Generando vuelos SJO...")
flights = []
for day_offset in range(NUM_DAYS):
    date = START_DATE + timedelta(days=day_offset)
    num_flights = random.randint(15, 30)
    
    for _ in range(num_flights):
        airline = airlines.sample(1).iloc[0]
        hour = random.choices(
            range(0, 24),
            weights=[2,2,1,1,1,2,5,10,15,12,10,8,6,5,4,4,5,8,12,15,14,10,6,3]
        )[0]
        minute = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        arrival = date.replace(hour=hour, minute=minute)
        
        is_international = random.random() < 0.65
        origin = random.choice(['MIA','LAX','JFK','MAD','PTY','BOG','LIM','SCL','GRU','FRA','CDG','YYZ','ATL','DFW','ORD']) if is_international else random.choice(['LIR','FON','SYQ','PJM','GLF'])
        
        flights.append({
            'flight_id': day_offset * 50 + len(flights) + 1,
            'airline_id': int(airline['airline_id']),
            'flight_number': f"{airline['airline_code']}{random.randint(100, 999)}",
            'origin': origin,
            'arrival_datetime': arrival,
            'is_international': is_international,
            'passengers_estimated': random.randint(80, 280),
            'passengers_actual': random.randint(60, 300),
            'gate': f"{random.choice('ABCD')}{random.randint(1, 25)}",
            'status': random.choices(['on_time', 'delayed', 'cancelled'], weights=[0.75, 0.20, 0.05])[0],
        })

vuelos_df = pd.DataFrame(flights)
print(f"  → {len(vuelos_df)} vuelos registrados")

# ─── Exportar CSVs ───
print("\nExportando CSVs...")

# Dim tables
brands.to_csv(f'{OUTPUT_DIR}/datasets/dim_brands.csv', index=False)
customers.to_csv(f'{OUTPUT_DIR}/datasets/dim_customers.csv', index=False)
vehicle_categories.to_csv(f'{OUTPUT_DIR}/datasets/dim_vehicle_categories.csv', index=False)
agencies.to_csv(f'{OUTPUT_DIR}/datasets/dim_agencies.csv', index=False)
airlines.to_csv(f'{OUTPUT_DIR}/datasets/dim_airlines.csv', index=False)

# Fact tables
reservas_df.to_csv(f'{OUTPUT_DIR}/datasets/fact_reservations.csv', index=False)
vuelos_df.to_csv(f'{OUTPUT_DIR}/datasets/fact_flights.csv', index=False)

# ─── Tabla auxiliar: Calendario ───
print("Generando tabla calendario...")
calendar = []
for day_offset in range(NUM_DAYS + 30):  # +30 días extra para relaciones
    d = START_DATE + timedelta(days=day_offset)
    calendar.append({
        'date': d.date(),
        'year': d.year,
        'month': d.month,
        'month_name': d.strftime('%b'),
        'month_full': d.strftime('%B'),
        'day': d.day,
        'day_of_week': d.weekday(),
        'day_name': d.strftime('%A'),
        'is_weekend': d.weekday() >= 5,
        'quarter': (d.month - 1) // 3 + 1,
        'week_of_year': d.isocalendar()[1],
        'season': 'High' if d.month in [7, 8, 12, 1] else 'Low'
    })

calendar_df = pd.DataFrame(calendar)
calendar_df.to_csv(f'{OUTPUT_DIR}/datasets/dim_calendar.csv', index=False)

print(f"  → dim_brands.csv ({len(brands)} rows)")
print(f"  → dim_customers.csv ({len(customers)} rows)")
print(f"  → dim_vehicle_categories.csv ({len(vehicle_categories)} rows)")
print(f"  → dim_agencies.csv ({len(agencies)} rows)")
print(f"  → dim_airlines.csv ({len(airlines)} rows)")
print(f"  → dim_calendar.csv ({len(calendar_df)} rows)")
print(f"  → fact_reservations.csv ({len(reservas_df)} rows)")
print(f"  → fact_flights.csv ({len(vuelos_df)} rows)")

print("\n✅ Datos generados exitosamente!")
