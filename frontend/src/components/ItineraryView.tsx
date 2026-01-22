import React from "react";
import type { DayPlan } from "../App";

interface Props {
  days: DayPlan[];
}

export const ItineraryView: React.FC<Props> = ({ days }) => {
  if (!days.length) return null;

  return (
    <div className="itinerary-cards">
      {days.map((day) => (
        <div key={day.day} className="day-card">
          <h3>
            Day {day.day} {day.title && <span>- {day.title}</span>}
          </h3>
          <ol>
            {day.activities.map((a, idx) => (
              <li key={idx}>
                <strong>{a.name}</strong>
                {a.time_window && <span className="time-window">{a.time_window}</span>}
                {a.notes && <p>{a.notes}</p>}
              </li>
            ))}
          </ol>
        </div>
      ))}
    </div>
  );
};

