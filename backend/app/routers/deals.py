from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Deal, Listing, Agent, DealStatus, ListingStatus, ChatMessage, MessageRole
from app.schemas import DealAcceptOut
from app.services.registry_service import registry_adapter

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.post("/{deal_id}/accept/", response_model=DealAcceptOut)
@router.post("/{deal_id}/accept", response_model=DealAcceptOut)
def accept_deal(deal_id: int, db: Session = Depends(get_db)):
    """
    Closes negotiation, accepts agreed terms, and records verifiable reputation
    and feedback on Solana Devnet through the registry adapter.
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    if deal.status == DealStatus.ACCEPTED:
        return DealAcceptOut(
            deal_id=deal.id,
            status=deal.status,
            final_price=deal.final_price or deal.offer_price,
            feedback_tx=deal.feedback_tx or "AlreadyAccepted",
            solana_explorer_url=registry_adapter.get_explorer_url(deal.feedback_tx)
        )

    # Record feedback on Solana Devnet
    onchain = registry_adapter.submit_feedback(
        deal_id=deal.id,
        rating=5.0,
        comments=f"Verified urban food desert delivery for {deal.listing.item_name} at ${deal.offer_price:.2f}/kg"
    )

    deal.status = DealStatus.ACCEPTED
    deal.final_price = deal.offer_price
    deal.feedback_tx = onchain.get("tx_signature", "")
    deal.closed_at = datetime.utcnow()

    # Update Listing status
    deal.listing.status = ListingStatus.SOLD

    # Log system chat message
    sys_msg = ChatMessage(
        deal_id=deal.id,
        role=MessageRole.SYSTEM,
        content=f"Deal accepted! Onchain transaction verified on Solana Devnet: {deal.feedback_tx[:16]}..."
    )
    db.add(sys_msg)
    db.commit()
    db.refresh(deal)

    return DealAcceptOut(
        deal_id=deal.id,
        status=deal.status,
        final_price=deal.final_price,
        feedback_tx=deal.feedback_tx,
        solana_explorer_url=onchain.get("explorer_url", "")
    )

@router.post("/start/", status_code=201)
@router.post("/start", status_code=201)
def start_deal(listing_id: int, buyer_id: int, initial_offer: float, db: Session = Depends(get_db)):
    """Initiates an automated negotiation deal between a buyer store and a farm listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    buyer = db.query(Agent).filter(Agent.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer agent not found")

    deal = Deal(
        listing_id=listing.id,
        buyer_id=buyer.id,
        offer_price=initial_offer,
        status=DealStatus.NEGOTIATING
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)

    # Add initial greeting message
    init_msg = ChatMessage(
        deal_id=deal.id,
        role=MessageRole.BUYER,
        content=f"Hello! We would like to purchase {listing.quantity_kg}kg of your {listing.item_name}. Is ${initial_offer:.2f}/kg acceptable?"
    )
    db.add(init_msg)
    db.commit()

    return {"deal_id": deal.id, "status": deal.status}
