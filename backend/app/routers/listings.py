import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Listing, Agent, AgentRole, ListingStatus
from app.schemas import ListingOut
from app.services.ai_service import ai_service

router = APIRouter(prefix="/listings", tags=["Listings"])

@router.post("/", response_model=ListingOut, status_code=201)
async def create_listing(
    seller_id: int = Form(...),
    quantity_kg: float = Form(...),
    floor_price: float = Form(2.00),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Farmer produce upload endpoint.
    Processes produce image with Google Gemma 4 via Gemini API.
    Saves listing with verified AI fields and seller agent identity.
    """
    seller = db.query(Agent).filter(Agent.id == seller_id, Agent.role == AgentRole.SELLER).first()
    if not seller:
        raise HTTPException(status_code=404, detail=f"Seller Agent with ID {seller_id} not found.")

    if quantity_kg <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0 kg.")

    # Read uploaded image bytes
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Multimodal analysis via Gemma 4
    mime_type = image.content_type or "image/jpeg"
    ai_result = ai_service.analyze_produce_image(image_bytes, mime_type)

    # Convert image to data URI so it renders immediately in frontend
    encoded_b64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:{mime_type};base64,{encoded_b64}"

    listing = Listing(
        seller_id=seller.id,
        image_url=image_url,
        item_name=ai_result["item_name"],
        grade=ai_result["grade"],
        freshness_notes=ai_result["freshness_notes"],
        description=ai_result["description"],
        suggested_price=ai_result["suggested_price_per_kg"],
        floor_price=floor_price,
        quantity_kg=quantity_kg,
        status=ListingStatus.ACTIVE
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

@router.get("/", response_model=list[ListingOut])
def list_listings(db: Session = Depends(get_db)):
    """Returns all active produce listings."""
    return db.query(Listing).filter(Listing.status == ListingStatus.ACTIVE).order_by(Listing.created_at.desc()).all()

@router.get("/{listing_id}", response_model=ListingOut)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Fetches details of a specific listing."""
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
