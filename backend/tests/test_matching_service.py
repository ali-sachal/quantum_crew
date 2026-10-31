from unittest.mock import MagicMock
from app.services.matching_service import haversine_distance_km, MatchingService

def test_haversine_distance():
    # Distance between NYC South Bronx (40.816, -73.918) and Central Harlem (40.8115, -73.9465)
    # is roughly 2.4 - 2.5 km
    dist = haversine_distance_km(40.8160, -73.9180, 40.8115, -73.9465)
    assert 2.0 < dist < 3.0

def test_store_ranking_prioritizes_high_deficit_and_close_distance():
    service = MatchingService()

    # Create dummy listing
    mock_seller = MagicMock()
    mock_seller.latitude = 40.8160
    mock_seller.longitude = -73.9180

    mock_listing = MagicMock()
    mock_listing.seller = mock_seller

    # Store A: Very close (40.8220, -73.9140) and High Deficit (South Bronx 10451)
    store_a = MagicMock()
    store_a.name = "Store A (Close & High Deficit)"
    store_a.latitude = 40.8220
    store_a.longitude = -73.9140
    store_a.zip_code = "10451"

    # Store B: Farther away and Low Deficit (Chelsea 10001)
    store_b = MagicMock()
    store_b.name = "Store B (Far & Low Deficit)"
    store_b.latitude = 40.7505
    store_b.longitude = -73.9934
    store_b.zip_code = "10001"

    ranked = service.rank_stores_for_listing(mock_listing, [store_a, store_b])

    assert len(ranked) == 2
    # Store A must rank higher than Store B
    assert ranked[0]["store"].name == store_a.name
    assert ranked[0]["match_score"] > ranked[1]["match_score"]

