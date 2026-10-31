from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Deal, ChatMessage, MessageRole, DealStatus
from app.schemas import ChatMessageOut, ChatSendRequest
from app.services.ai_service import ai_service

router = APIRouter(prefix="/chat", tags=["Negotiation Chat"])

@router.get("/{deal_id}/", response_model=list[ChatMessageOut])
@router.get("/{deal_id}", response_model=list[ChatMessageOut])
def get_chat_history(deal_id: int, db: Session = Depends(get_db)):
    """Fetches full chat history for a negotiation deal."""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    return db.query(ChatMessage).filter(ChatMessage.deal_id == deal_id).order_by(ChatMessage.created_at.asc()).all()

@router.post("/{deal_id}/", response_model=ChatMessageOut)
@router.post("/{deal_id}", response_model=ChatMessageOut)
def send_chat_message(deal_id: int, payload: ChatSendRequest, db: Session = Depends(get_db)):
    """
    Submits a buyer message to the negotiation session.
    Invokes Gemma 4 autonomous seller agent to formulate a guarded counteroffer or acceptance.
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    if deal.status != DealStatus.NEGOTIATING:
        raise HTTPException(status_code=400, detail="Cannot chat on a closed or accepted deal.")

    # 1. Save Buyer Message
    buyer_msg = ChatMessage(
        deal_id=deal.id,
        role=MessageRole.BUYER,
        content=payload.content.strip()
    )
    db.add(buyer_msg)
    db.commit()

    # 2. Retrieve Conversation Context
    all_msgs = db.query(ChatMessage).filter(ChatMessage.deal_id == deal.id).order_by(ChatMessage.created_at.asc()).all()
    history = [{"role": msg.role.value, "content": msg.content} for msg in all_msgs]

    # 3. Call Gemma 4 AI Service with Floor Price Guardrails
    reply_content = ai_service.negotiate(
        chat_history=history,
        floor_price=deal.listing.floor_price,
        item_name=deal.listing.item_name
    )

    # 4. Save AI Seller Agent Reply
    seller_msg = ChatMessage(
        deal_id=deal.id,
        role=MessageRole.SELLER_AGENT,
        content=reply_content
    )
    db.add(seller_msg)
    db.commit()
    db.refresh(seller_msg)

    return seller_msg
