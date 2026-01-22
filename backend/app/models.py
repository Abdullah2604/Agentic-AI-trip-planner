from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .db import Base


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    destination = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, index=True, nullable=True)
    tags = Column(String, nullable=True)  # comma-separated tags
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    popularity = Column(Float, nullable=True)
    price_bucket = Column(String, nullable=True)  # e.g. $, $$, $$$
    opening_hours = Column(String, nullable=True)


class DistanceMatrix(Base):
    __tablename__ = "distance_matrix"

    id = Column(Integer, primary_key=True, index=True)
    from_attraction_id = Column(Integer, ForeignKey("attractions.id"), index=True)
    to_attraction_id = Column(Integer, ForeignKey("attractions.id"), index=True)
    distance_km = Column(Float, nullable=True)
    duration_min = Column(Float, nullable=True)


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    prompt = Column(Text, nullable=False)
    destination = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    itinerary_text = Column(Text, nullable=False)
    itinerary_json = Column(Text, nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5
    comments = Column(Text, nullable=True)
    raw_payload = Column(Text, nullable=True)

