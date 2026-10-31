import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FoodMatch API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # AI Service - Google Gemma 4 via Gemini API
    # Must be read strictly from environment variable, never guessed or hardcoded
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMMA_MODEL_ID: str = os.getenv("GEMMA_MODEL_ID", "")

    # Snowflake & CoCo Configuration
    SNOWFLAKE_ACCOUNT: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    SNOWFLAKE_USER: str = os.getenv("SNOWFLAKE_USER", "")
    SNOWFLAKE_PASSWORD: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    SNOWFLAKE_WAREHOUSE: str = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "")
    SNOWFLAKE_SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

    # Solana Agent Registry & Devnet
    SOLANA_RPC_URL: str = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
    SOLANA_PRIVATE_KEY: str = os.getenv("SOLANA_PRIVATE_KEY", "")
    SOLANA_REGISTRY_PROGRAM_ID: str = os.getenv("SOLANA_REGISTRY_PROGRAM_ID", "")

    # Matching Weights (configurable in settings)
    MATCH_WEIGHT_DEFICIT: float = float(os.getenv("MATCH_WEIGHT_DEFICIT", "0.6"))
    MATCH_WEIGHT_DISTANCE: float = float(os.getenv("MATCH_WEIGHT_DISTANCE", "0.4"))

    # SQLite Database for Local Development
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./foodmatch.db")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

