from __future__ import annotations

from typing import Dict, Any

from sqlalchemy.orm import Session

from ..models import Itinerary
from ..ranker import rank as rank_candidates
from .candidates import get_candidates
from .llm import extract_preferences, generate_itinerary


def plan_trip(db: Session, prompt: str) -> Dict[str, Any]:
    # 1. Preference extraction
    prefs = extract_preferences(prompt)

    destination = prefs["destination"]
    days = int(prefs["days"])
    interests = prefs.get("interests") or []
    budget = prefs.get("budget")

    # 2. Fetch candidates from DB
    candidates = get_candidates(
        db,
        destination=destination,
        interests=interests,
        budget=budget,
        days=days,
    )

    if not candidates:
        raise ValueError("No candidate attractions found for the given destination.")

    # 3. Ranking
    ranked = rank_candidates(candidates, prefs)

    # 4. Itinerary generation
    itinerary_text, itinerary_json = generate_itinerary(prompt, prefs, ranked)

    # 5. Persist itinerary
    itinerary = Itinerary(
        prompt=prompt,
        destination=destination,
        days=days,
        itinerary_text=itinerary_text,
        itinerary_json=str(itinerary_json),
    )
    db.add(itinerary)
    db.flush()  # assign ID

    return {
        "itinerary_id": itinerary.id,
        "prefs": prefs,
        "itinerary_text": itinerary_text,
        "itinerary_json": itinerary_json,
        "ranked_attractions": ranked,
    }

