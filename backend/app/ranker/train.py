from __future__ import annotations

"""
Simple training script for a learning-to-rank style model.

For now this demonstrates how you could:
  * generate pseudo-labels from heuristic scores
  * fit an ML model (e.g., RandomForestRegressor)
  * persist it to disk for use in `ranker.py`

The main API that the backend uses remains `rank()` in `ranker.py`,
so this script is optional and can be run offline.
"""

from pathlib import Path
from typing import List

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import select

from ..db import db_session
from ..models import Attraction
from .ranker import _heuristic_score, UserPrefs


MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODELS_DIR / "ranker_rf.pkl"


def _featurize(attraction: Attraction) -> List[float]:
    return [
        float(attraction.rating or 4.0),
        float(attraction.popularity or 0.5),
    ]


def train_from_db() -> None:
    with db_session() as db:
        rows = db.execute(select(Attraction)).scalars().all()

        if not rows:
            print("No attractions in DB; nothing to train on.")
            return

        prefs = UserPrefs(
            destination="Dubai",
            days=3,
            interests=["landmarks", "shopping", "food"],
            budget=None,
        )

        X = []
        y = []

        for a in rows:
            feat = _featurize(a)
            score = _heuristic_score(
                {
                    "rating": a.rating,
                    "popularity": a.popularity,
                    "category": a.category,
                    "tags": a.tags,
                    "price_bucket": a.price_bucket,
                },
                prefs,
            )
            X.append(feat)
            y.append(score)

        X_arr = np.array(X)
        y_arr = np.array(y)

        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_arr, y_arr)

        joblib.dump(model, MODEL_PATH)
        print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train_from_db()

