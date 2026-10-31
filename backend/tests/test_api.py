from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.seed import run_seed

client = TestClient(app)

def setup_module(module):
    """Seed test database before API tests run."""
    run_seed()

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_listings():
    response = client.get("/api/listings/")
    assert response.status_code == 200
    listings = response.json()
    assert len(listings) > 0
    assert "item_name" in listings[0]
    assert "seller" in listings[0]

def test_get_demand_deficit():
    response = client.get("/api/demand/?zip=10451")
    assert response.status_code == 200
    scores = response.json()
    assert len(scores) == 7
    days = [d["day"] for d in scores]
    assert "Friday" in days

def test_get_matches_for_listing():
    response = client.get("/api/matches/1/")
    assert response.status_code == 200
    matches = response.json()
    assert len(matches) > 0
    assert "match_score" in matches[0]

def test_chat_negotiation():
    payload = {"content": "Can we buy this batch at $2.30/kg?"}
    response = client.post("/api/chat/1/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "seller_agent"
    assert len(data["content"]) > 0

def test_accept_deal_onchain():
    response = client.post("/api/deals/1/accept/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert "solana_explorer_url" in data
    assert "feedback_tx" in data

