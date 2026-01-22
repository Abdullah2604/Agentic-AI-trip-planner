from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import get_settings
from .db import Base, engine, get_db, db_session
from .models import Attraction, Feedback
from .schemas import FeedbackPayload, PlanRequest, PlanResponse, RankedAttraction
from .data.seed_dubai import seed_dubai_attractions
from .services.itinerary import plan_trip


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Agentic AI Trip Planner API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Create tables if they don't exist yet
    Base.metadata.create_all(bind=engine)
    # Seed initial Dubai attractions for MVP
    with db_session() as db:
        seed_dubai_attractions(db)


@app.post("/plan", response_model=PlanResponse)
def create_plan(payload: PlanRequest, db: Session = Depends(get_db)) -> PlanResponse:
    try:
        result = plan_trip(db, payload.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - generic fallback
        raise HTTPException(status_code=500, detail="Failed to generate itinerary") from exc

    ranked = [
        RankedAttraction(
            id=a["id"],
            name=a["name"],
            score=a["score"],
            latitude=a["latitude"],
            longitude=a["longitude"],
            category=a.get("category"),
        )
        for a in result["ranked_attractions"]
    ]

    return PlanResponse(
        itinerary_text=result["itinerary_text"],
        itinerary_json=result["itinerary_json"],
        ranked_attractions=ranked,
    )


@app.get("/attractions")
def list_attractions(db: Session = Depends(get_db)):
    rows = db.query(Attraction).limit(100).all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "destination": a.destination,
            "category": a.category,
            "latitude": a.latitude,
            "longitude": a.longitude,
        }
        for a in rows
    ]


@app.post("/feedback")
def submit_feedback(payload: FeedbackPayload, db: Session = Depends(get_db)):
    fb = Feedback(
        itinerary_id=payload.itinerary_id,
        rating=payload.rating,
        comments=payload.comments,
        raw_payload=str(payload.raw_payload) if payload.raw_payload is not None else None,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return {"id": fb.id}

