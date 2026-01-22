import React, { useState } from "react";
import axios from "axios";
import { MapView } from "./components/MapView";
import { ItineraryView } from "./components/ItineraryView";

export interface Activity {
  name: string;
  lat: number;
  lng: number;
  time_window?: string | null;
  notes?: string | null;
}

export interface DayPlan {
  day: number;
  title?: string | null;
  activities: Activity[];
}

export interface PlanResponse {
  itinerary_text: string;
  itinerary_json: DayPlan[];
}

const API_BASE = "http://localhost:8000";

const App: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PlanResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await axios.post<PlanResponse>(`${API_BASE}/plan`, {
        prompt
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to generate itinerary");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Agentic AI Trip Planner</h1>
        <p>Describe your ideal Dubai trip. The agent will plan your days and map it.</p>
      </header>

      <main className="app-main">
        <section className="left-panel">
          <form onSubmit={handleSubmit} className="prompt-form">
            <label htmlFor="prompt">Trip prompt</label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Example: 3 days in Dubai with focus on views, malls, and some culture. Mid-budget."
            />
            <button type="submit" disabled={loading}>
              {loading ? "Planning..." : "Plan my trip"}
            </button>
          </form>

          {error && <div className="error-banner">{error}</div>}

          {result && (
            <section className="itinerary-section">
              <h2>Itinerary</h2>
              <pre className="itinerary-text">{result.itinerary_text}</pre>
              <ItineraryView days={result.itinerary_json} />
            </section>
          )}
        </section>

        <section className="right-panel">
          <h2>Map</h2>
          <div className="map-wrapper">
            <MapView days={result?.itinerary_json ?? []} />
          </div>
        </section>
      </main>
    </div>
  );
};

export default App;

