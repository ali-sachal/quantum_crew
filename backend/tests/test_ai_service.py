import pytest
from app.services.ai_service import AIService

def test_ai_response_parser_valid():
    service = AIService()
    sample_json = """
    {
        "item_name": "Hydroponic Butterhead Lettuce",
        "grade": "A",
        "freshness_notes": "Crisp leaves, roots attached in mineral solution.",
        "description": "Butter-soft organic lettuce heads.",
        "suggested_price_per_kg": 3.75
    }
    """
    result = service._parse_and_validate_analysis_json(sample_json)
    assert result["item_name"] == "Hydroponic Butterhead Lettuce"
    assert result["grade"] == "A"
    assert result["suggested_price_per_kg"] == 3.75

def test_ai_response_parser_markdown_wrapped():
    service = AIService()
    sample_text = """
    Here is your produce analysis:
    ```json
    {
        "item_name": "Organic Red Radishes",
        "grade": "b",
        "freshness_notes": "Bright pink skin with fresh greens.",
        "description": "Peppery fresh radishes.",
        "suggested_price_per_kg": "2.20"
    }
    ```
    Thank you!
    """
    result = service._parse_and_validate_analysis_json(sample_text)
    assert result["item_name"] == "Organic Red Radishes"
    assert result["grade"] == "B"  # Normalized to uppercase
    assert result["suggested_price_per_kg"] == 2.20

def test_ai_response_parser_missing_fields_raises_error():
    service = AIService()
    invalid_json = '{"item_name": "Carrots"}'
    with pytest.raises(ValueError):
        service._parse_and_validate_analysis_json(invalid_json)

def test_negotiation_guardrail_floor_price():
    service = AIService()
    floor_price = 2.50
    # Simulate buyer proposing an offer below floor price
    history = [
        {"role": "buyer", "content": "Can you sell these at $1.80/kg?"}
    ]
    reply = service.negotiate(history, floor_price, "Roma Tomatoes")
    # Reply must not accept $1.80 and must mention the floor price or counteroffer >= 2.50
    assert "$1.80" not in reply or "floor" in reply.lower() or "sustain" in reply.lower()
