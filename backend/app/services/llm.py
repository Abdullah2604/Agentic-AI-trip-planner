from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from ..config import get_settings


settings = get_settings()

# Initialize Gemini if API key is available
if GEMINI_AVAILABLE and settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)


def _stub_extract_prefs(prompt: str) -> Dict[str, Any]:
    """Very simple preference extractor used when no LLM key is configured.

    In production this would call OpenAI / Anthropic / Mistral to parse out
    destination, days, interests, and budget from free-form text.
    """
    destination = "Dubai"
    days = 3
    interests: List[str] = []
    budget = None

    lower = prompt.lower()
    if "museum" in lower:
        interests.append("museum")
    if "food" in lower or "restaurant" in lower:
        interests.append("food")
    if "shopping" in lower or "mall" in lower:
        interests.append("shopping")
    if "adventure" in lower or "theme park" in lower:
        interests.append("adventure")

    if "budget" in lower or "cheap" in lower or "low cost" in lower:
        budget = "low"
    elif "luxury" in lower or "5-star" in lower or "expensive" in lower:
        budget = "high"

    return {
        "destination": destination,
        "days": days,
        "interests": interests or ["landmarks"],
        "budget": budget,
    }


def _gemini_extract_prefs(prompt: str) -> Dict[str, Any]:
    """Use Gemini to extract structured preferences from user prompt."""
    if not GEMINI_AVAILABLE or not genai:
        return _stub_extract_prefs(prompt)
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        system_prompt = """You are a travel assistant. Extract structured information from the user's trip request.

Return ONLY a valid JSON object with these exact keys:
{
  "destination": "string (city name, default to 'Dubai' if not specified)",
  "days": number (integer, default to 3 if not specified),
  "interests": ["string"] (array of interest keywords like: shopping, food, museum, adventure, landmarks, culture, beach, nightlife),
  "budget": "low" | "mid" | "high" | null
}

Example inputs and outputs:
Input: "3 days in Dubai, I love shopping and food"
Output: {"destination": "Dubai", "days": 3, "interests": ["shopping", "food"], "budget": null}

Input: "Budget trip to Dubai for 2 days, museums and culture"
Output: {"destination": "Dubai", "days": 2, "interests": ["museum", "culture"], "budget": "low"}

Now extract from this user request:"""

        response = model.generate_content(
            f"{system_prompt}\n\nUser request: {prompt}\n\nJSON:"
        )
        
        # Extract JSON from response
        text = response.text.strip()
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(text)
        
        # Validate and set defaults
        return {
            "destination": result.get("destination", "Dubai"),
            "days": int(result.get("days", 3)),
            "interests": result.get("interests", ["landmarks"]),
            "budget": result.get("budget"),
        }
    except Exception as e:
        print(f"Gemini API error in extract_preferences: {e}")
        # Fall back to stub
        return _stub_extract_prefs(prompt)


def extract_preferences(prompt: str) -> Dict[str, Any]:
    """Extract structured user preferences from the free-form prompt.
    
    Uses Gemini API if available, otherwise falls back to rule-based extraction.
    """
    if GEMINI_AVAILABLE and settings.gemini_api_key:
        return _gemini_extract_prefs(prompt)
    return _stub_extract_prefs(prompt)


def _gemini_generate_itinerary(
    prompt: str,
    prefs: Dict[str, Any],
    ranked_attractions: List[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    """Use Gemini to generate a natural itinerary text and structured JSON."""
    if not GEMINI_AVAILABLE or not genai:
        return _template_generate_itinerary(prompt, prefs, ranked_attractions)
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        # Prepare attractions list for the prompt
        attractions_info = "\n".join([
            f"- {attr['name']} ({attr.get('category', 'attraction')}): {attr.get('description', 'No description')} [Location: {attr['latitude']}, {attr['longitude']}]"
            for attr in ranked_attractions[:20]  # Limit to top 20
        ])
        
        system_prompt = f"""You are a travel planning assistant. Create a detailed {prefs.get('days', 3)}-day itinerary for {prefs.get('destination', 'Dubai')}.

User's original request: {prompt}
Interests: {', '.join(prefs.get('interests', []))}
Budget: {prefs.get('budget', 'mid')}

Available attractions:
{attractions_info}

Create a realistic day-by-day itinerary that:
1. Groups nearby attractions logically
2. Includes 3-5 activities per day
3. Suggests reasonable time windows (e.g., "9:00 AM - 11:00 AM")
4. Provides helpful notes about each activity

Return your response in this EXACT JSON format:
{{
  "itinerary_text": "A well-formatted text description of the itinerary with day-by-day breakdown",
  "itinerary_json": [
    {{
      "day": 1,
      "title": "Day 1: [descriptive title]",
      "activities": [
        {{
          "name": "Attraction Name",
          "lat": 25.2048,
          "lng": 55.2708,
          "time_window": "9:00 AM - 11:00 AM",
          "notes": "Helpful tips or description"
        }}
      ]
    }}
  ]
}}

Make sure the lat/lng match the attractions provided. Return ONLY valid JSON."""

        response = model.generate_content(system_prompt)
        
        # Extract JSON from response
        text = response.text.strip()
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(text)
        
        itinerary_text = result.get("itinerary_text", "")
        itinerary_json = result.get("itinerary_json", [])
        
        # Validate structure
        if not isinstance(itinerary_json, list):
            raise ValueError("itinerary_json must be a list")
        
        return itinerary_text, itinerary_json
        
    except Exception as e:
        print(f"Gemini API error in generate_itinerary: {e}")
        # Fall back to template-based generation
        return _template_generate_itinerary(prompt, prefs, ranked_attractions)


def _template_generate_itinerary(
    prompt: str,
    prefs: Dict[str, Any],
    ranked_attractions: List[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    """Template-based itinerary generation (fallback when LLM is unavailable)."""
    days = int(prefs.get("days", 1))
    per_day = max(1, min(6, len(ranked_attractions) // days or 1))

    itinerary_json: List[Dict[str, Any]] = []
    lines: List[str] = []

    idx = 0
    for day in range(1, days + 1):
        day_activities: List[Dict[str, Any]] = []
        lines.append(f"Day {day}:")

        for _ in range(per_day):
            if idx >= len(ranked_attractions):
                break
            attr = ranked_attractions[idx]
            idx += 1
            lines.append(f" - {attr['name']} ({attr.get('category', 'attraction')})")
            day_activities.append(
                {
                    "name": attr["name"],
                    "lat": attr["latitude"],
                    "lng": attr["longitude"],
                    "time_window": None,
                    "notes": attr.get("description") or "",
                }
            )

        itinerary_json.append(
            {
                "day": day,
                "title": f"Day {day} in {prefs.get('destination', 'your destination')}",
                "activities": day_activities,
            }
        )
        lines.append("")

    itinerary_text = "\n".join(lines).strip()
    return itinerary_text, itinerary_json


def generate_itinerary(
    prompt: str,
    prefs: Dict[str, Any],
    ranked_attractions: List[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    """Generate itinerary text + JSON from ranked attractions.
    
    Uses Gemini API if available, otherwise falls back to template-based generation.
    """
    if GEMINI_AVAILABLE and settings.gemini_api_key:
        return _gemini_generate_itinerary(prompt, prefs, ranked_attractions)
    return _template_generate_itinerary(prompt, prefs, ranked_attractions)

