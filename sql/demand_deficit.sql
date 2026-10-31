-- ============================================================
-- FoodMatch: Weekly Fresh Food Deficit Prediction Query
-- Analyzes low-income urban zip codes and computes the deficit score
-- based on household income, grocery vs fresh spend ratio, and corner store concentration.
-- ============================================================

WITH zip_stats AS (
    SELECT
        d.zip_code,
        d.neighborhood_name,
        d.total_population,
        d.median_household_income,
        d.food_insecurity_index,
        s.day_of_week,
        s.avg_grocery_spend_per_capita,
        s.avg_fresh_produce_spend_per_capita,
        s.corner_store_count,
        s.supermarket_count,
        -- Produce availability ratio: fraction of grocery spend on fresh produce
        (s.avg_fresh_produce_spend_per_capita / NULLIF(s.avg_grocery_spend_per_capita, 0)) AS fresh_ratio,
        -- Supermarket access deficit factor
        (s.corner_store_count / NULLIF(s.supermarket_count + 1, 0)) AS bodega_dominance_ratio
    FROM neighborhood_demographics d
    JOIN weekly_food_spending_patterns s ON d.zip_code = s.zip_code
    WHERE d.zip_code = %(zip_code)s
)
SELECT
    day_of_week,
    -- Deficit Score from 0.0 (No deficit) to 10.0 (Severe food desert deficit)
    ROUND(
        LEAST(
            10.0,
            GREATEST(
                0.0,
                -- 40% Weight: Food insecurity base index
                (food_insecurity_index * 0.40) +
                -- 35% Weight: Lack of fresh produce spending share on that specific day
                ((1.0 - COALESCE(fresh_ratio, 0.1)) * 3.5) +
                -- 25% Weight: Income vulnerability factor
                ((1.0 - LEAST(median_household_income / 75000.0, 1.0)) * 2.5)
            )
        ),
        2
    ) AS deficit_score,
    neighborhood_name,
    total_population
FROM zip_stats
ORDER BY 
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END ASC;

