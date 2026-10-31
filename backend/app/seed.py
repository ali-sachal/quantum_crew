from app.database import engine, SessionLocal, Base
from app.models import Agent, Listing, Deal, ChatMessage, AgentRole, ListingStatus, DealStatus, MessageRole
from app.services.registry_service import registry_adapter

def run_seed():
    """
    Seeds database with authentic urban community gardens, corner stores,
    listings analyzed by Gemma 4, active negotiations, and verified Solana devnet identities.
    """
    print("Re-creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    print("Seeding verified agents (Community Gardens & Corner Stores)...")

    # 1. Urban Farms / Community Gardens (Sellers)
    f1 = Agent(
        role=AgentRole.SELLER,
        name="South Bronx Green Workers Co-op",
        description="Hydroponic and raised bed urban agriculture collective in Mott Haven.",
        latitude=40.8160,
        longitude=-73.9180,
        zip_code="10451",
        solana_address="SolanaFarmBx1111111111111111111111111111111",
        registry_tx="5xSeedRegBxFarm9876543210devnetExplorerTxHash1",
        reputation_score=4.9
    )

    f2 = Agent(
        role=AgentRole.SELLER,
        name="Harlem Roots Rooftop Farm",
        description="Certified pesticide-free organic rooftop produce on 125th St.",
        latitude=40.8115,
        longitude=-73.9465,
        zip_code="10027",
        solana_address="SolanaFarmHarlem222222222222222222222222222",
        registry_tx="5xSeedRegHarlemFarm9876543210devnetExplorerTx2",
        reputation_score=4.8
    )

    f3 = Agent(
        role=AgentRole.SELLER,
        name="East New York Farms! Collective",
        description="Youth-led urban agroecology project growing culturally appropriate crops.",
        latitude=40.6650,
        longitude=-73.8820,
        zip_code="11208",
        solana_address="SolanaFarmENY333333333333333333333333333333",
        registry_tx="5xSeedRegENYFarm9876543210devnetExplorerTx3",
        reputation_score=4.95
    )

    # 2. Corner Stores / Bodegas in Food Deserts (Buyers)
    s1 = Agent(
        role=AgentRole.BUYER,
        name="Melrose Fresh Grocery & Bodega",
        description="Local corner store committed to expanding fresh produce in South Bronx.",
        latitude=40.8220,
        longitude=-73.9140,
        zip_code="10451",
        solana_address="SolanaStoreMelrose3333333333333333333333333",
        registry_tx="5xSeedRegMelroseStore9876543210devnetTx4",
        reputation_score=4.7
    )

    s2 = Agent(
        role=AgentRole.BUYER,
        name="149th St Mini Market & Deli",
        description="High-traffic neighborhood bodega near subway station with new refrigerated produce cooler.",
        latitude=40.8175,
        longitude=-73.9215,
        zip_code="10455",
        solana_address="SolanaStore149th4444444444444444444444444444",
        registry_tx="5xSeedReg149thStore9876543210devnetTx5",
        reputation_score=4.9
    )

    s3 = Agent(
        role=AgentRole.BUYER,
        name="Harlem Oasis Convenience",
        description="Family-owned grocery stocking staple foods and organic produce.",
        latitude=40.8090,
        longitude=-73.9490,
        zip_code="10027",
        solana_address="SolanaStoreHarlem55555555555555555555555555",
        registry_tx="5xSeedRegHarlemStore9876543210devnetTx6",
        reputation_score=4.6
    )

    db.add_all([f1, f2, f3, s1, s2, s3])
    db.commit()

    print("Seeding verified listings with Gemma 4 inspected produce...")

    # 3. Produce Listings
    l1 = Listing(
        seller_id=f1.id,
        image_url="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop",
        item_name="Vine-Ripened Roma Tomatoes",
        grade="A",
        freshness_notes="Plump, taut skin, bright scarlet hue. Harvested this morning.",
        description="Sweet, firm Roma tomatoes perfect for daily cooking and fresh sandwiches.",
        suggested_price=3.20,
        floor_price=2.20,
        quantity_kg=45.0,
        status=ListingStatus.ACTIVE
    )

    l2 = Listing(
        seller_id=f2.id,
        image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&auto=format&fit=crop",
        item_name="Tuscan Lacinato Kale Bunches",
        grade="A",
        freshness_notes="Deep forest green, zero wilting, high leaf turgor and mineral density.",
        description="Freshly bunched organic dinosaur kale, great for health-conscious shoppers.",
        suggested_price=2.90,
        floor_price=2.00,
        quantity_kg=30.0,
        status=ListingStatus.ACTIVE
    )

    l3 = Listing(
        seller_id=f1.id,
        image_url="https://images.unsplash.com/photo-1566385101042-1a0aa0c1268c?w=600&auto=format&fit=crop",
        item_name="Crisp Bell Peppers (Mixed Tri-Color)",
        grade="B",
        freshness_notes="Slight cosmetic variation in shape, exceptionally crunchy and sweet flesh.",
        description="Tri-color red, yellow, and green bell peppers for quick stir fry or salads.",
        suggested_price=2.60,
        floor_price=1.80,
        quantity_kg=55.0,
        status=ListingStatus.ACTIVE
    )

    l4 = Listing(
        seller_id=f3.id,
        image_url="https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=600&auto=format&fit=crop",
        item_name="Organic Calaloo & Mustard Greens",
        grade="A",
        freshness_notes="Pesticide-free tender leaves, ideal Caribbean and Southern staple.",
        description="Culturally resonant nutritious greens tailored for urban neighborhood recipes.",
        suggested_price=3.40,
        floor_price=2.40,
        quantity_kg=40.0,
        status=ListingStatus.ACTIVE
    )

    db.add_all([l1, l2, l3, l4])
    db.commit()

    print("Seeding active demo negotiation and onchain deal...")

    # 4. Active Deal & Negotiation
    d1 = Deal(
        listing_id=l1.id,
        buyer_id=s1.id,
        offer_price=2.50,
        status=DealStatus.NEGOTIATING
    )
    db.add(d1)
    db.commit()

    m1 = ChatMessage(
        deal_id=d1.id,
        role=MessageRole.BUYER,
        content="Hello! We are looking to buy 40kg of your Roma tomatoes for our Friday rush. Can you do $2.00/kg?"
    )
    m2 = ChatMessage(
        deal_id=d1.id,
        role=MessageRole.SELLER_AGENT,
        content="Hello Melrose Fresh! As a community farm collective, our absolute floor cost is $2.20/kg. For 40kg, we can offer $2.50/kg delivered fresh Friday morning!"
    )
    db.add_all([m1, m2])
    db.commit()

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    run_seed()

