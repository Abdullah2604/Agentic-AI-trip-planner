from __future__ import annotations

from sqlalchemy.orm import Session

from ..models import Attraction


SEED_ATTRACTIONS = [
    {
        "name": "Burj Khalifa",
        "description": "Iconic skyscraper with observation deck overlooking Dubai.",
        "category": "landmark",
        "tags": "landmark,skydeck,views",
        "latitude": 25.1972,
        "longitude": 55.2744,
        "rating": 4.8,
        "popularity": 0.99,
        "price_bucket": "$$$",
    },
    {
        "name": "The Dubai Mall",
        "description": "One of the world's largest shopping malls with entertainment and dining.",
        "category": "shopping",
        "tags": "shopping,mall,food,entertainment",
        "latitude": 25.1985,
        "longitude": 55.2796,
        "rating": 4.7,
        "popularity": 0.97,
        "price_bucket": "$$",
    },
    {
        "name": "Dubai Marina Walk",
        "description": "Scenic waterfront walkway with cafes and restaurants.",
        "category": "waterfront",
        "tags": "waterfront,food,walking,views",
        "latitude": 25.0792,
        "longitude": 55.1403,
        "rating": 4.6,
        "popularity": 0.9,
        "price_bucket": "$$",
    },
    {
        "name": "Dubai Museum",
        "description": "Museum located in Al Fahidi Fort showcasing Dubai's history.",
        "category": "museum",
        "tags": "museum,history,culture",
        "latitude": 25.2637,
        "longitude": 55.2972,
        "rating": 4.4,
        "popularity": 0.8,
        "price_bucket": "$",
    },
    {
        "name": "Desert Safari",
        "description": "Evening desert safari with dune bashing and BBQ dinner.",
        "category": "adventure",
        "tags": "adventure,desert,safari",
        "latitude": 24.9670,
        "longitude": 55.2040,
        "rating": 4.7,
        "popularity": 0.92,
        "price_bucket": "$$",
    },
]


def seed_dubai_attractions(db: Session) -> None:
    existing = (
        db.query(Attraction)
        .filter(Attraction.destination == "Dubai")
        .count()
    )
    if existing > 0:
        return

    for item in SEED_ATTRACTIONS:
        db.add(
            Attraction(
                name=item["name"],
                destination="Dubai",
                description=item["description"],
                category=item["category"],
                tags=item["tags"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                rating=item["rating"],
                popularity=item["popularity"],
                price_bucket=item["price_bucket"],
            )
        )
    db.commit()

