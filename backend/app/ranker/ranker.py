from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

import math


@dataclass
class UserPrefs:
    destination: str
    days: int
    interests: List[str]
    budget: str | None = None


def _category_match_score(attraction: Dict[str, Any], prefs: UserPrefs) -> float:
    tags = (attraction.get("tags") or "").lower()
    category = (attraction.get("category") or "").lower()
    score = 0.0
    for interest in prefs.interests:
        if interest.lower() in tags or interest.lower() in category:
            score += 1.0
    return score


def _heuristic_score(attraction: Dict[str, Any], prefs: UserPrefs) -> float:
    rating = float(attraction.get("rating") or 4.0)
    popularity = float(attraction.get("popularity") or 0.5)
    cat_score = _category_match_score(attraction, prefs)

    base = rating / 5.0 * 0.5 + popularity * 0.3 + cat_score * 0.2

    # Simple budget compatibility penalty (placeholder)
    price_bucket = (attraction.get("price_bucket") or "").strip()
    if prefs.budget and price_bucket:
        if prefs.budget == "low" and price_bucket in {"$$$", "$$$$"}:
            base *= 0.8
        elif prefs.budget == "high" and price_bucket in {"$", "$$"}:
            base *= 0.9

    return base


def rank(candidates: Iterable[Dict[str, Any]], user_prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Rank candidate attractions using a simple heuristic.

    This is the interface the backend relies on. It can later be
    replaced by an AutoML / sklearn-based implementation that
    preserves the same function signature.
    """
    prefs = UserPrefs(
        destination=user_prefs.get("destination", ""),
        days=int(user_prefs.get("days", 1)),
        interests=list(user_prefs.get("interests") or []),
        budget=user_prefs.get("budget"),
    )

    scored: List[Dict[str, Any]] = []
    for attr in candidates:
        score = _heuristic_score(attr, prefs)
        attr_with_score = dict(attr)
        attr_with_score["score"] = float(score)
        scored.append(attr_with_score)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

