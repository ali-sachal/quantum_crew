import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base

class AgentRole(str, enum.Enum):
    SELLER = "seller"
    BUYER = "buyer"

class ListingStatus(str, enum.Enum):
    ACTIVE = "active"
    MATCHED = "matched"
    SOLD = "sold"

class DealStatus(str, enum.Enum):
    NEGOTIATING = "negotiating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"

class MessageRole(str, enum.Enum):
    BUYER = "buyer"
    SELLER_AGENT = "seller_agent"
    SYSTEM = "system"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(AgentRole), nullable=False)
    name = Column(String(120), nullable=False)
    description = Column(String(255), default="")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    zip_code = Column(String(10), nullable=False, index=True)
    solana_address = Column(String(88), nullable=True)
    registry_tx = Column(String(120), nullable=True)
    reputation_score = Column(Float, default=4.8)
    created_at = Column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="seller")
    deals = relationship("Deal", back_populates="buyer")

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    item_name = Column(String(120), nullable=False)
    grade = Column(String(2), nullable=False)  # A, B, or C
    freshness_notes = Column(Text, default="")
    description = Column(Text, default="")
    suggested_price = Column(Float, nullable=False)
    floor_price = Column(Float, nullable=False, default=1.80)
    quantity_kg = Column(Float, nullable=False)
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

    seller = relationship("Agent", back_populates="listings")
    deals = relationship("Deal", back_populates="listing")

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    offer_price = Column(Float, nullable=False)
    final_price = Column(Float, nullable=True)
    status = Column(Enum(DealStatus), default=DealStatus.NEGOTIATING)
    feedback_tx = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    listing = relationship("Listing", back_populates="deals")
    buyer = relationship("Agent", back_populates="deals")
    messages = relationship("ChatMessage", back_populates="deal")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal", back_populates="messages")
