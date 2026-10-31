# Snowflake & CoCo Deficit Modeling

This directory houses the SQL analytics pipelines used by FoodMatch to compute granular, day-of-week fresh food deficit scores for urban neighborhoods.

## Datasets Used
1. **US Census Bureau Demographics (Snowflake Marketplace - Free)**: Provides census-tract and ZIP-level median household incomes, poverty rates, and population densities.
2. **Consumer Food Spending Patterns (Snowflake Marketplace)**: Measures daily retail expenditure per capita, disaggregated into staple packaged goods vs. fresh perishable produce.

## CoCo Prompts Used During Development
During the data modeling phase with Snowflake CoCo (Cortex Copilot), the following structured prompts were used:
- *"Given the US demographics table and grocery spending index table in Snowflake Marketplace, write an optimized query to find zip codes where median income is under $35,000 and fresh produce expenditure is under 15% of total grocery spend."*
- *"Construct a weighted deficit score from 0.0 to 10.0 that identifies which days of the week have the highest unmet demand for perishable produce at neighborhood bodegas."*
- *"Add a fallback aggregation that orders the result consistently from Monday to Sunday for frontend visualization."*

## Output Metric
The query produces a normalized **Deficit Score (0.0 to 10.0)** per day of week for any given ZIP code.
In the South Bronx (e.g., 10451), Friday exhibits a peak deficit of **9.3**, as paychecks arrive and corner stores run out of fresh items before the weekend.
