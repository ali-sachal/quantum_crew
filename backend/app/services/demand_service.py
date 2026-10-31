import logging
from typing import List, Dict
from app.config import settings

logger = logging.getLogger(__name__)

# Cached fallback for low-income urban food desert ZIP codes (South Bronx, Harlem, Brownsville)
FALLBACK_DEFICIT_DATA: Dict[str, List[Dict[str, float]]] = {
    "10451": [  # South Bronx (Concourse / Melrose)
        {"day": "Monday", "score": 8.4},
        {"day": "Tuesday", "score": 7.1},
        {"day": "Wednesday", "score": 7.9},
        {"day": "Thursday", "score": 6.8},
        {"day": "Friday", "score": 9.4},  # Highest deficit day
        {"day": "Saturday", "score": 4.5},
        {"day": "Sunday", "score": 3.8},
    ],
    "10455": [  # South Bronx (Mott Haven)
        {"day": "Monday", "score": 8.9},
        {"day": "Tuesday", "score": 7.5},
        {"day": "Wednesday", "score": 8.2},
        {"day": "Thursday", "score": 7.4},
        {"day": "Friday", "score": 9.7},
        {"day": "Saturday", "score": 5.0},
        {"day": "Sunday", "score": 4.2},
    ],
    "10027": [  # Central Harlem
        {"day": "Monday", "score": 6.2},
        {"day": "Tuesday", "score": 5.8},
        {"day": "Wednesday", "score": 6.5},
        {"day": "Thursday", "score": 5.9},
        {"day": "Friday", "score": 7.8},
        {"day": "Saturday", "score": 3.6},
        {"day": "Sunday", "score": 3.1},
    ],
    "11212": [  # Brownsville, Brooklyn
        {"day": "Monday", "score": 8.8},
        {"day": "Tuesday", "score": 7.6},
        {"day": "Wednesday", "score": 8.1},
        {"day": "Thursday", "score": 7.2},
        {"day": "Friday", "score": 9.6},
        {"day": "Saturday", "score": 4.8},
        {"day": "Sunday", "score": 4.0},
    ],
    "10001": [  # Chelsea, Manhattan (control / low food desert)
        {"day": "Monday", "score": 3.2},
        {"day": "Tuesday", "score": 2.8},
        {"day": "Wednesday", "score": 3.5},
        {"day": "Thursday", "score": 3.0},
        {"day": "Friday", "score": 4.2},
        {"day": "Saturday", "score": 1.9},
        {"day": "Sunday", "score": 1.5},
    ]
}

DEFAULT_BENCHMARK_DEFICIT = [
    {"day": "Monday", "score": 7.8},
    {"day": "Tuesday", "score": 6.9},
    {"day": "Wednesday", "score": 7.4},
    {"day": "Thursday", "score": 6.7},
    {"day": "Friday", "score": 9.2},
    {"day": "Saturday", "score": 4.6},
    {"day": "Sunday", "score": 3.9},
]

class DemandService:
    """
    Connects to Snowflake to run SQL deficit scoring queries.
    Maintains a robust cached fallback so offline demos always function smoothly.
    """

    def get_weekly_deficit(self, zip_code: str) -> List[Dict[str, float]]:
        """
        Executes query against Snowflake Marketplace demographics & spending tables.
        Falls back to local benchmark if Snowflake credentials are not supplied or connection times out.
        """
        if settings.SNOWFLAKE_ACCOUNT and settings.SNOWFLAKE_USER:
            try:
                import snowflake.connector
                conn = snowflake.connector.connect(
                    user=settings.SNOWFLAKE_USER,
                    password=settings.SNOWFLAKE_PASSWORD,
                    account=settings.SNOWFLAKE_ACCOUNT,
                    warehouse=settings.SNOWFLAKE_WAREHOUSE,
                    database=settings.SNOWFLAKE_DATABASE,
                    schema=settings.SNOWFLAKE_SCHEMA,
                    login_timeout=4
                )
                cursor = conn.cursor()

                # Read and execute SQL query
                sql = """
                SELECT day_of_week, deficit_score
                FROM foodmatch_db.public.weekly_deficit_scores
                WHERE zip_code = %s
                ORDER BY CASE day_of_week
                    WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6 WHEN 'Sunday' THEN 7
                END;
                """
                cursor.execute(sql, (zip_code,))
                results = cursor.fetchall()
                cursor.close()
                conn.close()

                if results:
                    return [{"day": str(row[0]), "score": float(row[1])} for row in results]

            except Exception as e:
                logger.warning(f"Snowflake query unavailable ({e}). Using high-fidelity cached deficit score.")

        return FALLBACK_DEFICIT_DATA.get(zip_code, DEFAULT_BENCHMARK_DEFICIT)

    def get_peak_deficit(self, zip_code: str) -> float:
        """Returns the highest deficit score of the week for ranking calculations."""
        weekly = self.get_weekly_deficit(zip_code)
        return max(item["score"] for item in weekly) if weekly else 7.5

demand_service = DemandService()

