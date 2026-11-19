-- =============================================================================
-- Programación Análisis de Datos (PAD)
-- Consultas SQLite de ejemplo para el dataset:
--   "Financial Transactions Dataset: Analytics" (Kaggle)
--
-- Base de datos objetivo: data/proyecto.sqlite
-- Generada mediante:      python src/crear_db.py
--
-- Tablas esperadas (a partir de los CSV del dataset):
--   - transactions_data : registros de transacciones financieras
--   - cards_data        : información de tarjetas de crédito/débito
--   - users_data        : perfil demográfico y financiero de clientes
--
-- Nota técnica sobre valores monetarios:
--   En el dataset original, columnas como `amount`, `credit_limit`,
--   `yearly_income`, `per_capita_income` y `total_debt` incluyen el símbolo `$`
--   (por ejemplo: '$14.57' o '$-77.00'). Por ello, en las consultas analíticas
--   se limpian al vuelo con: CAST(REPLACE(REPLACE(col, '$', ''), ',', '') AS REAL).
-- =============================================================================


-- -----------------------------------------------------------------------------
-- 1. EXPLORACIÓN DEL ESQUEMA (METADATOS DE SQLITE)
-- -----------------------------------------------------------------------------

-- 1.1 Listar todas las tablas disponibles en la base de datos
SELECT name AS tabla, type AS tipo
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

-- 1.2 Inspeccionar la estructura (columnas y tipos) de cada tabla principal
PRAGMA table_info(transactions_data);
PRAGMA table_info(cards_data);
PRAGMA table_info(users_data);


-- -----------------------------------------------------------------------------
-- 2. VOLUMEN DE REGISTROS Y VISTA PREVIA
-- -----------------------------------------------------------------------------

-- 2.1 Conteo de filas por tabla principal
SELECT 'transactions_data' AS tabla, COUNT(*) AS total_registros FROM transactions_data
UNION ALL
SELECT 'cards_data'        AS tabla, COUNT(*) AS total_registros FROM cards_data
UNION ALL
SELECT 'users_data'        AS tabla, COUNT(*) AS total_registros FROM users_data;

-- 2.2 Muestra rápida de las primeras 10 transacciones
SELECT *
FROM transactions_data
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 3. ESTADÍSTICAS BÁSICAS DE MONTOS TRANSACCIONADOS
-- -----------------------------------------------------------------------------

-- 3.1 Resumen general de montos (incluyendo devoluciones o montos negativos)
SELECT
    COUNT(*)                                                                 AS total_transacciones,
    ROUND(SUM(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_total,
    ROUND(AVG(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_promedio,
    ROUND(MIN(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_minimo,
    ROUND(MAX(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_maximo,
    SUM(
        CASE
            WHEN CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL) < 0 THEN 1
            ELSE 0
        END
    )                                                                        AS transacciones_negativas
FROM transactions_data;


-- -----------------------------------------------------------------------------
-- 4. ANÁLISIS POR CANAL DE PAGO (use_chip) Y ERRORES DE TRANSACCIÓN
-- -----------------------------------------------------------------------------

-- 4.1 Distribución de transacciones por método de captura (Swipe, Chip, Online)
SELECT
    use_chip                                                                 AS canal_pago,
    COUNT(*)                                                                 AS num_transacciones,
    ROUND(
        100.0 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM transactions_data), 0),
        2
    )                                                                        AS porcentaje,
    ROUND(AVG(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS ticket_promedio
FROM transactions_data
GROUP BY use_chip
ORDER BY num_transacciones DESC;

-- 4.2 Tipos de errores más frecuentes registrados en las transacciones
SELECT
    errors                                                                   AS tipo_error,
    COUNT(*)                                                                 AS ocurrencias,
    ROUND(AVG(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_promedio
FROM transactions_data
WHERE errors IS NOT NULL
  AND TRIM(errors) != ''
GROUP BY errors
ORDER BY ocurrencias DESC
LIMIT 15;


-- -----------------------------------------------------------------------------
-- 5. ANÁLISIS GEOGRÁFICO Y POR CATEGORÍA DE COMERCIO (MCC)
-- -----------------------------------------------------------------------------

-- 5.1 Top 15 estados con mayor número de transacciones
SELECT
    merchant_state                                                           AS estado,
    COUNT(*)                                                                 AS num_transacciones,
    ROUND(SUM(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_total,
    ROUND(AVG(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS ticket_promedio
FROM transactions_data
WHERE merchant_state IS NOT NULL
  AND TRIM(merchant_state) != ''
GROUP BY merchant_state
ORDER BY num_transacciones DESC
LIMIT 15;

-- 5.2 Top 15 códigos MCC por monto total transaccionado
SELECT
    mcc,
    COUNT(*)                                                                 AS num_transacciones,
    ROUND(SUM(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_total,
    ROUND(AVG(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS ticket_promedio
FROM transactions_data
GROUP BY mcc
ORDER BY monto_total DESC
LIMIT 15;


-- -----------------------------------------------------------------------------
-- 6. EVOLUCIÓN TEMPORAL DE TRANSACCIONES
-- -----------------------------------------------------------------------------

-- 6.1 Volumen y monto total de transacciones por año
SELECT
    SUBSTR(date, 1, 4)                                                       AS anio,
    COUNT(*)                                                                 AS num_transacciones,
    ROUND(SUM(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_total,
    ROUND(AVG(CAST(REPLACE(REPLACE(amount, '$', ''), ',', '') AS REAL)), 2)  AS ticket_promedio
FROM transactions_data
WHERE date IS NOT NULL
GROUP BY anio
ORDER BY anio;


-- -----------------------------------------------------------------------------
-- 7. CONSULTAS RELACIONALES (JOIN) ENTRE TRANSACCIONES, TARJETAS Y CLIENTES
-- -----------------------------------------------------------------------------

-- 7.1 Volumen y gasto promedio por marca y tipo de tarjeta
SELECT
    c.card_brand                                                               AS marca_tarjeta,
    c.card_type                                                                AS tipo_tarjeta,
    COUNT(t.id)                                                                AS num_transacciones,
    ROUND(SUM(CAST(REPLACE(REPLACE(t.amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_total,
    ROUND(AVG(CAST(REPLACE(REPLACE(t.amount, '$', ''), ',', '') AS REAL)), 2)  AS ticket_promedio
FROM transactions_data AS t
INNER JOIN cards_data AS c
    ON t.card_id = c.id
GROUP BY c.card_brand, c.card_type
ORDER BY monto_total DESC;

-- 7.2 Top 10 clientes por monto total gastado junto con su perfil financiero
SELECT
    u.id                                                                       AS client_id,
    u.gender                                                                   AS genero,
    u.current_age                                                              AS edad,
    u.credit_score                                                             AS puntaje_credito,
    u.yearly_income                                                            AS ingreso_anual,
    u.total_debt                                                               AS deuda_total,
    COUNT(t.id)                                                                AS num_transacciones,
    ROUND(SUM(CAST(REPLACE(REPLACE(t.amount, '$', ''), ',', '') AS REAL)), 2)  AS monto_total
FROM transactions_data AS t
INNER JOIN users_data AS u
    ON t.client_id = u.id
GROUP BY
    u.id,
    u.gender,
    u.current_age,
    u.credit_score,
    u.yearly_income,
    u.total_debt
ORDER BY monto_total DESC
LIMIT 10;

-- 7.3 Resumen de tarjetas por marca: límite de crédito promedio y exposición
SELECT
    card_brand                                                                      AS marca_tarjeta,
    card_type                                                                       AS tipo_tarjeta,
    COUNT(*)                                                                        AS total_tarjetas,
    ROUND(AVG(CAST(REPLACE(REPLACE(credit_limit, '$', ''), ',', '') AS REAL)), 2)   AS limite_credito_promedio,
    SUM(CASE WHEN UPPER(has_chip) = 'YES' THEN 1 ELSE 0 END)                        AS tarjetas_con_chip
FROM cards_data
GROUP BY card_brand, card_type
ORDER BY total_tarjetas DESC;


-- -----------------------------------------------------------------------------
-- 8. OPTIMIZACIÓN OPCIONAL CON ÍNDICES
--    Descomenta y ejecuta estas sentencias si deseas acelerar los JOIN y filtros
--    sobre `transactions_data` (también puedes generarlos con:
--    `python src/crear_db.py --crear-indices`).
-- -----------------------------------------------------------------------------
-- CREATE INDEX IF NOT EXISTS idx_transactions_data_client_id ON transactions_data (client_id);
-- CREATE INDEX IF NOT EXISTS idx_transactions_data_card_id   ON transactions_data (card_id);
-- CREATE INDEX IF NOT EXISTS idx_transactions_data_date      ON transactions_data (date);
-- CREATE INDEX IF NOT EXISTS idx_transactions_data_mcc       ON transactions_data (mcc);
-- CREATE INDEX IF NOT EXISTS idx_cards_data_client_id        ON cards_data (client_id);
