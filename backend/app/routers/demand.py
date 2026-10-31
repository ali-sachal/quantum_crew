from fastapi import APIRouter, Query
from app.schemas import DayDeficit
from app.services.demand_service import demand_service

router = APIRouter(prefix="/demand", tags=["Demand Prediction"])

@router.get("/", response_model=list[DayDeficit])
def get_demand_deficit(zip: str = Query("10451", description="US 5-digit ZIP code for urban neighborhood")):
    """
    Returns weekly fresh food deficit scores per day of week (Monday to Sunday)
    calculated via Snowflake consumer-spending & census data pipeline.
    """
    return demand_service.get_weekly_deficit(zip)
