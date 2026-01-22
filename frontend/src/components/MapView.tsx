import React, { useMemo } from "react";
import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
import L from "leaflet";
import type { DayPlan } from "../App";

interface Props {
  days: DayPlan[];
}

const defaultCenter: [number, number] = [25.2048, 55.2708]; // Dubai

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export const MapView: React.FC<Props> = ({ days }) => {
  const allPoints = useMemo(
    () =>
      days.flatMap((d) =>
        d.activities.map((a) => [a.lat, a.lng] as [number, number])
      ),
    [days]
  );

  const center = allPoints[0] ?? defaultCenter;

  return (
    <MapContainer center={center} zoom={12} className="map-root">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
      />

      {days.map((day) => {
        const coords = day.activities.map(
          (a) => [a.lat, a.lng] as [number, number]
        );
        return (
          <React.Fragment key={day.day}>
            {coords.map((pos, idx) => (
              <Marker key={`${day.day}-${idx}`} position={pos} icon={markerIcon}>
                <Popup>
                  <strong>{day.activities[idx].name}</strong>
                  {day.activities[idx].notes && (
                    <div style={{ marginTop: 4 }}>{day.activities[idx].notes}</div>
                  )}
                </Popup>
              </Marker>
            ))}
            {coords.length > 1 && (
              <Polyline positions={coords} color="#2b6cb0" weight={3} />
            )}
          </React.Fragment>
        );
      })}
    </MapContainer>
  );
};

