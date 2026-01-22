from __future__ import annotations

"""
Data refresh module.

For the MVP, this simply (re)seeds a small Dubai attractions set.
In a fuller implementation, this would:
  * pull fresh data from an external API or CSV
  * normalize fields
  * compute distance_matrix entries
  * upsert into SQLite
"""

from sqlalchemy.orm import Session

from ..db import db_session
from .seed_dubai import seed_dubai_attractions


def refresh_all(db: Session | None = None) -> None:
    """Run a full data refresh.

    If a DB session is passed, use it; otherwise create a temporary one.
    """
    if db is not None:
        seed_dubai_attractions(db)
        return

    with db_session() as session:
        seed_dubai_attractions(session)


if __name__ == "__main__":
    # Allow manual one-off refresh via `python -m app.data.refresh`
    refresh_all()

