from __future__ import annotations

from app.ranker import rank


def test_ranker_orders_by_score_descending():
    candidates = [
        {
            "id": 1,
            "name": "Low Rated",
            "rating": 3.0,
            "popularity": 0.2,
            "category": "museum",
            "tags": "museum,history",
        },
        {
            "id": 2,
            "name": "Highly Rated",
            "rating": 4.8,
            "popularity": 0.9,
            "category": "landmark",
            "tags": "landmark,views",
        },
    ]
    prefs = {
        "destination": "Dubai",
        "days": 3,
        "interests": ["landmark"],
        "budget": None,
    }

    ranked = rank(candidates, prefs)

    assert ranked[0]["id"] == 2
    assert ranked[1]["id"] == 1

