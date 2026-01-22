from typing import List, Optional

from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    prompt: str = Field(..., description="Free-form user request describing the trip preferences")


class Activity(BaseModel):
    name: str
    lat: float
    lng: float
    time_window: Optional[str] = None
    notes: Optional[str] = None


class DayPlan(BaseModel):
    day: int
    title: Optional[str] = None
    activities: List[Activity]


class RankedAttraction(BaseModel):
    id: int
    name: str
    score: float
    latitude: float
    longitude: float
    category: Optional[str] = None


class PlanResponse(BaseModel):
    itinerary_text: str
    itinerary_json: List[DayPlan]
    ranked_attractions: Optional[List[RankedAttraction]] = None


class FeedbackPayload(BaseModel):
    itinerary_id: Optional[int] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    comments: Optional[str] = None
    raw_payload: Optional[dict] = None

