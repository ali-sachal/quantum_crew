from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Listing, Agent, AgentRole
from app.schemas import MatchResult
from app.services.matching_service import matching_service

router = APIRouter(prefix="/matches", tags=["Matching"])

@router.get("/{listing_id}/", response_model=list[MatchResult])
@router.get("/{listing_id}", response_model=list[MatchResult])
def get_matches_for_listing(listing_id: int, db: Session = Depends(get_db)):
    """
    Ranks buyer corner stores for a given produce listing using:
    - Neighborhood fresh food deficit from Snowflake
    - Haversine distance between farm and store
    """
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    candidate_stores = db.query(Agent).filter(Agent.role == AgentRole.BUYER).all()
    if not candidate_stores:
        return []

    return matching_service.rank_stores_for_listing(listing, candidate_stores)

