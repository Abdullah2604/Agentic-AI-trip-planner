from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Attraction


def get_candidates(
    db: Session,
    destination: str,
    interests: List[str],
    budget: str | None,
    days: int,
    limit: int = 60,
) -> List[Dict[str, Any]]:
    stmt = select(Attraction).where(Attraction.destination == destination)
    rows = db.execute(stmt).scalars().all()

    candidates: List[Dict[str, Any]] = []
    for row in rows:
        candidates.append(
            {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "category": row.category,
                "tags": row.tags,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "rating": row.rating,
                "popularity": row.popularity,
                "price_bucket": row.price_bucket,
                "opening_hours": row.opening_hours,
            }
        )

    # Simple truncation for MVP
    return candidates[:limit]

