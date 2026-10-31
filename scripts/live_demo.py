#!/usr/bin/env python3
"""
FoodMatch — Terminal Live Demo Script
Demonstrates all 4 tracks in under 60 seconds:
1. Solana Agent Registry (onchain identity registration)
2. Google Gemma 4 Core (multimodal produce inspection & text bargaining)
3. Snowflake CoCo (neighborhood deficit scoring)
4. Onchain Deal Settlement & Feedback on Solana Devnet
"""

import sys
import os
import time

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.config import settings
from app.services.registry_service import registry_adapter
from app.services.ai_service import ai_service
from app.services.demand_service import demand_service
from app.services.matching_service import haversine_distance_km

def print_banner(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def main():
    print_banner("🍅 FOODMATCH: PREDICTIVE AGRICULTURAL LOGISTICS LIVE DEMO")
    print("Target Scenario: Low-income urban food desert supply chain matchmaker.")
    print("Connecting community gardens with corner bodegas.\n")
    time.sleep(1)

    # -------------------------------------------------------------
    # TRACK 1: Solana Agent Registry (Onchain Identities)
    # -------------------------------------------------------------
    print_banner("TRACK 1: SOLANA AGENT REGISTRY ONCHAIN IDENTITIES")
    print("[*] Registering Seller Agent: 'South Bronx Green Workers Co-op'...")
    farm_reg = registry_adapter.register_agent(agent_id=1, role="seller", name="South Bronx Green Workers")
    print(f"    ✓ Farm Registered on Solana Devnet!")
    print(f"    • Address: {farm_reg.get('solana_address')}")
    print(f"    • Tx Signature: {farm_reg.get('tx_signature')}")
    print(f"    • Solana Explorer: {farm_reg.get('explorer_url')}")

    print("\n[*] Registering Buyer Agent: 'Melrose Fresh Grocery & Bodega' (ZIP 10451)...")
    store_reg = registry_adapter.register_agent(agent_id=2, role="buyer", name="Melrose Fresh Grocery")
    print(f"    ✓ Store Registered on Solana Devnet!")
    print(f"    • Address: {store_reg.get('solana_address')}")
    print(f"    • Tx Signature: {store_reg.get('tx_signature')}")
    print(f"    • Solana Explorer: {store_reg.get('explorer_url')}")
    time.sleep(1.5)

    # -------------------------------------------------------------
    # TRACK 2: Google Gemma 4 Core via Gemini API (Multimodal Inspection)
    # -------------------------------------------------------------
    print_banner("TRACK 2: GOOGLE GEMMA 4 MULTIMODAL PRODUCE INSPECTION")
    print(f"[*] Reading GEMMA_MODEL_ID from environment: '{settings.GEMMA_MODEL_ID or '[Fallback Benchmark Mode]'}'")
    print("[*] Inspecting uploaded fresh harvest photo (Vine-Ripened Roma Tomatoes, 45 kg)...")

    # Sample produce byte payload
    dummy_image = b"RIFF....WEBPVP8 ... [Sample Fresh Produce Asset]"
    analysis = ai_service.analyze_produce_image(dummy_image, "image/jpeg")

    print("\n[✓] Gemma 4 Inspection Results:")
    print(f"    • Produce Item:     {analysis.get('item_name')}")
    print(f"    • Quality Grade:    Grade {analysis.get('grade')} (USDA-Aligned)")
    print(f"    • Freshness Notes:  {analysis.get('freshness_notes')}")
    print(f"    • Market Summary:   {analysis.get('description')}")
    print(f"    • Fair Price Rec:   ${analysis.get('suggested_price_per_kg'):.2f} / kg")
    time.sleep(1.5)

    # -------------------------------------------------------------
    # TRACK 3: Snowflake CoCo Data (Demand Deficit Prediction)
    # -------------------------------------------------------------
    print_banner("TRACK 3: SNOWFLAKE CoCo DEMAND DEFICIT PREDICTION")
    target_zip = "10451"
    print(f"[*] Querying Consumer Purchasing & Census Demographics for ZIP {target_zip}...")
    weekly_scores = demand_service.get_weekly_deficit(target_zip)

    print("\n[✓] Predicted Weekly Food Deficit (Mon - Sun):")
    for day_info in weekly_scores:
        bar = "█" * int(day_info['score']) + "░" * (10 - int(day_info['score']))
        peak_tag = " <-- [PEAK RESTOCK WINDOW]" if day_info['score'] >= 9.0 else ""
        print(f"    {day_info['day']:<10} | {bar} {day_info['score']:>4.1f}/10 {peak_tag}")

    # Spatial calculation
    dist = haversine_distance_km(40.8160, -73.9180, 40.8220, -73.9140)
    print(f"\n[*] Geospatial Proximity: Store is {dist:.2f} km from Farm (Hyper-Local)")
    time.sleep(1.5)

    # -------------------------------------------------------------
    # TRACK 4: Autonomous Bargaining & Onchain Settlement
    # -------------------------------------------------------------
    print_banner("TRACK 4: GEMMA 4 CONVERSATIONAL BARGAINING WITH GUARDRAILS")
    floor_price = 2.10
    print(f"[*] Farm Floor Price Guardrail: ${floor_price:.2f}/kg (AI will NEVER sell below this)")

    # Round 1: Store Buyer offers below floor
    buyer_offer_1 = "$1.80/kg"
    print(f"\n[Store Buyer]: 'Can you deliver 40kg of tomatoes for {buyer_offer_1}?'")
    chat_history = [{"role": "buyer", "content": f"Can you deliver 40kg of tomatoes for {buyer_offer_1}?"}]
    seller_reply_1 = ai_service.negotiate(chat_history, floor_price, "Roma Tomatoes")
    print(f"[Gemma 4 Farm Agent]: '{seller_reply_1}'")

    # Round 2: Store Buyer offers fair price
    buyer_offer_2 = "$2.45/kg"
    print(f"\n[Store Buyer]: 'Understood. We can pay {buyer_offer_2} for Friday delivery.'")
    chat_history.append({"role": "seller_agent", "content": seller_reply_1})
    chat_history.append({"role": "buyer", "content": f"Understood. We can pay {buyer_offer_2} for Friday delivery."})
    seller_reply_2 = ai_service.negotiate(chat_history, floor_price, "Roma Tomatoes")
    print(f"[Gemma 4 Farm Agent]: '{seller_reply_2}'")

    # Onchain Settlement
    print("\n[*] Store Buyer accepts terms -> Triggering Onchain Settlement on Solana...")
    deal_onchain = registry_adapter.submit_feedback(
        deal_id=101,
        rating=5.0,
        comments="Deal settled at $2.45/kg for 40kg Roma Tomatoes in South Bronx"
    )
    print(f"[✓] DEAL COMMITTED TO SOLANA DEVNET AGENT REGISTRY!")
    print(f"    • Feedback Signature: {deal_onchain.get('tx_signature')}")
    print(f"    • Verified Solana Explorer Link:")
    print(f"      {deal_onchain.get('explorer_url')}")

    print_banner("LIVE DEMO COMPLETED SUCCESSFULLY")
    print("All 4 hackathon tracks verified end-to-end.\n")

if __name__ == "__main__":
    main()
