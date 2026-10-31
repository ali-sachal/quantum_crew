from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models import AgentRole, ListingStatus, DealStatus, MessageRole

class AgentBase(BaseModel):
    name: str
    role: AgentRole
    description: Optional[str] = ""
    latitude: float
    longitude: float
    zip_code: str

class AgentCreate(AgentBase):
    pass

class AgentOut(AgentBase):
    id: int
    solana_address: Optional[str] = None
    registry_tx: Optional[str] = None
    reputation_score: float = 4.8
    created_at: datetime

    class Config:
        from_attributes = True

class ListingCreate(BaseModel):
    seller_id: int
    quantity_kg: float = Field(..., gt=0)
    floor_price: Optional[float] = Field(default=1.80, gt=0)

class ListingOut(BaseModel):
    id: int
    seller: AgentOut
    image_url: str
    item_name: str
    grade: str
    freshness_notes: str
    description: str
    suggested_price: float
    floor_price: float
    quantity_kg: float
    status: ListingStatus
    created_at: datetime

    class Config:
        from_attributes = True

class DayDeficit(BaseModel):
    day: str
    score: float

class MatchResult(BaseModel):
    store: AgentOut
    distance_km: float
    peak_deficit: float
    match_score: float

class ChatMessageOut(BaseModel):
    id: int
    role: MessageRole
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSendRequest(BaseModel):
    content: str

class DealAcceptOut(BaseModel):
    deal_id: int
    status: DealStatus
    final_price: float
    feedback_tx: str
    solana_explorer_url: str
