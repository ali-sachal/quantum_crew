import math
from typing import List, Dict, Any
from app.config import settings
from app.services.demand_service import demand_service

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0  # Earth's radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class MatchingService:
    """
    Ranks buyer stores for a given produce listing based on:
    1. Neighborhood unmet deficit (from Snowflake demand model)
    2. Geographic proximity (Haversine distance)
    Weights are configurable via settings.MATCH_WEIGHT_DEFICIT and settings.MATCH_WEIGHT_DISTANCE.
    """

    def rank_stores_for_listing(self, listing: Any, stores: List[Any]) -> List[Dict[str, Any]]:
        w_deficit = settings.MATCH_WEIGHT_DEFICIT
        w_distance = settings.MATCH_WEIGHT_DISTANCE

        ranked_results = []

        for store in stores:
            distance_km = haversine_distance_km(
                listing.seller.latitude, listing.seller.longitude,
                store.latitude, store.longitude
            )

            peak_deficit = demand_service.get_peak_deficit(store.zip_code)

            # Proximity score: 1.0 (at same location) decaying to 0.0 at 25km radius
            max_effective_radius_km = 25.0
            proximity_score = max(0.0, 1.0 - (distance_km / max_effective_radius_km))

            # Deficit normalization: scale 0.0-10.0 mapped to 0.0-1.0
            normalized_deficit = min(max(peak_deficit / 10.0, 0.0), 1.0)

            composite_score = round(
                (w_deficit * normalized_deficit) + (w_distance * proximity_score),
                3
            )

            ranked_results.append({
                "store": store,
                "distance_km": round(distance_km, 2),
                "peak_deficit": round(peak_deficit, 1),
                "match_score": composite_score
            })

        # Sort descending by match score
        return sorted(ranked_results, key=lambda x: x["match_score"], reverse=True)

matching_service = MatchingService()

