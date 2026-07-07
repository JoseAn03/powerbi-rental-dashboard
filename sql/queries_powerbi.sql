-- ============================================
-- Power BI - Consultas SQL Optimizadas
-- Proyecto: Rental Operations Dashboard
-- ============================================

-- ═══════════════════════════════════════════════
-- 1. GAMEPLAN DIARIO - Reservas del día actual
-- ═══════════════════════════════════════════════
SELECT 
    ROW_NUMBER() OVER (PARTITION BY b.brand_name ORDER BY r.pickup_datetime) AS letra,
    r.reservation_id,
    CONCAT(b.brand_name, ' //') AS marca,
    CASE 
        WHEN c.is_vip = 1 THEN '* MAIN VIP*'
        WHEN a.agency_name = 'Expedia' THEN '* EXPEDIA*'
        WHEN c.is_corporate = 1 THEN '* CORPORATE*'
        ELSE ''
    END AS tipo_vip,
    CONCAT(c.first_name, ' ', c.last_name) AS cliente,
    DATE_FORMAT(r.pickup_datetime, '%H:%i') AS hora_recogida,
    vc.category_name AS tipo_vehiculo,
    r.rental_days AS dias,
    r.total_amount AS monto
FROM fact_reservations r
JOIN dim_brands b ON r.brand_id = b.brand_id
JOIN dim_customers c ON r.customer_id = c.customer_id
JOIN dim_vehicle_categories vc ON r.category_id = vc.category_id
LEFT JOIN dim_agencies a ON r.agency_id = a.agency_id
WHERE DATE(r.pickup_datetime) = CURDATE() 
  AND r.status = 'activa'
ORDER BY b.brand_name, r.pickup_datetime;

-- ═══════════════════════════════════════════════
-- 2. NO-SHOW ANALYSIS - Análisis de No-Shows
-- ═══════════════════════════════════════════════
SELECT 
    b.brand_name,
    DATE_FORMAT(r.pickup_datetime, '%Y-%m') AS mes,
    COUNT(*) AS total_reservas,
    SUM(CASE WHEN r.status = 'no_show' THEN 1 ELSE 0 END) AS no_shows,
    ROUND(
        SUM(CASE WHEN r.status = 'no_show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        1
    ) AS no_show_pct,
    ROUND(AVG(r.total_amount), 2) AS avg_ticket,
    SUM(r.total_amount) AS revenue_total,
    -- Pérdida estimada por No-Shows
    ROUND(
        SUM(CASE WHEN r.status = 'no_show' THEN r.total_amount ELSE 0 END), 
        2
    ) AS perdida_no_show
FROM fact_reservations r
JOIN dim_brands b ON r.brand_id = b.brand_id
GROUP BY b.brand_name, DATE_FORMAT(r.pickup_datetime, '%Y-%m')
ORDER BY mes, b.brand_name;

-- ═══════════════════════════════════════════════
-- 3. ANÁLISIS POR HORA - Horas pico de recogida
-- ═══════════════════════════════════════════════
SELECT 
    HOUR(r.pickup_datetime) AS hora,
    b.brand_name,
    COUNT(*) AS reservas,
    ROUND(AVG(r.total_amount), 2) AS ticket_promedio
FROM fact_reservations r
JOIN dim_brands b ON r.brand_id = b.brand_id
WHERE r.status IN ('activa', 'completada')
GROUP BY HOUR(r.pickup_datetime), b.brand_name
ORDER BY hora, b.brand_name;

-- ═══════════════════════════════════════════════
-- 4. KPI DIARIOS - Dashboard ejecutivo
-- ═══════════════════════════════════════════════
SELECT 
    DATE(r.pickup_datetime) AS fecha,
    COUNT(*) AS reservas_totales,
    COUNT(DISTINCT r.customer_id) AS clientes_unicos,
    SUM(CASE WHEN r.status = 'no_show' THEN 1 ELSE 0 END) AS no_shows,
    SUM(CASE WHEN r.status = 'cancelada' THEN 1 ELSE 0 END) AS cancelaciones,
    ROUND(AVG(r.rental_days), 1) AS avg_duracion,
    ROUND(SUM(r.total_amount), 2) AS revenue_total,
    ROUND(AVG(r.total_amount), 2) AS ticket_promedio,
    SUM(CASE WHEN r.is_vip = 1 THEN 1 ELSE 0 END) AS reservas_vip,
    SUM(CASE WHEN r.is_corporate = 1 THEN 1 ELSE 0 END) AS reservas_corp
FROM fact_reservations r
GROUP BY DATE(r.pickup_datetime)
ORDER BY fecha;

-- ═══════════════════════════════════════════════
-- 5. TOP AGENCIAS - Rentabilidad por canal
-- ═══════════════════════════════════════════════
SELECT 
    a.agency_name,
    COUNT(*) AS reservas,
    ROUND(SUM(r.total_amount), 2) AS revenue_bruto,
    ROUND(SUM(r.total_amount) * a.commission_pct / 100, 2) AS comision,
    ROUND(SUM(r.total_amount) * (100 - a.commission_pct) / 100, 2) AS revenue_neto,
    ROUND(AVG(r.total_amount), 2) AS ticket_promedio,
    ROUND(
        SUM(CASE WHEN r.status = 'no_show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
        1
    ) AS no_show_pct
FROM fact_reservations r
JOIN dim_agencies a ON r.agency_id = a.agency_id
GROUP BY a.agency_name, a.commission_pct
ORDER BY reservas DESC;

-- ═══════════════════════════════════════════════
-- 6. FLUJO DE VUELOS SJO - Conexión con llegadas
-- ═══════════════════════════════════════════════
SELECT 
    DATE(f.arrival_datetime) AS fecha,
    COUNT(*) AS vuelos_totales,
    SUM(CASE WHEN f.is_international = 1 THEN 1 ELSE 0 END) AS vuelos_internacionales,
    SUM(CASE WHEN f.is_international = 0 THEN 1 ELSE 0 END) AS vuelos_nacionales,
    SUM(f.passengers_actual) AS pasajeros_totales,
    ROUND(AVG(f.passengers_actual), 0) AS avg_pasajeros,
    SUM(CASE WHEN f.status = 'delayed' THEN 1 ELSE 0 END) AS vuelos_retrasados,
    ROUND(
        SUM(CASE WHEN f.status = 'delayed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        1
    ) AS retraso_pct
FROM fact_flights f
GROUP BY DATE(f.arrival_datetime)
ORDER BY fecha;

-- ═══════════════════════════════════════════════
-- 7. COMPARATIVA GRUPOS - Enterprise vs Grupo ANC
-- ═══════════════════════════════════════════════
SELECT 
    b.group,
    ROUND(AVG(r.total_amount), 2) AS ticket_promedio,
    ROUND(AVG(r.rental_days), 1) AS duracion_promedio,
    COUNT(*) AS total_reservas,
    ROUND(
        SUM(CASE WHEN r.status = 'no_show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        1
    ) AS no_show_pct,
    ROUND(SUM(r.total_amount), 2) AS revenue_total
FROM fact_reservations r
JOIN dim_brands b ON r.brand_id = b.brand_id
GROUP BY b.group
ORDER BY revenue_total DESC;
