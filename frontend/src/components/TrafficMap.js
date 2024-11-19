import React from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

const TrafficMap = ({ incidents, trafficFlow, center }) => {
  return (
    <MapContainer
      center={center}
      zoom={12}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {/* Render incidents */}
      {incidents.map((incident) => (
        <Marker
          key={incident.id}
          position={[incident.latitude, incident.longitude]}
        >
          <Popup>
            <div>
              <h3 className="font-semibold">{incident.type}</h3>
              <p>{incident.description}</p>
              <p>Severity: {incident.severity}</p>
            </div>
          </Popup>
        </Marker>
      ))}

      {/* Render traffic flow */}
      {trafficFlow.map((flow, index) => (
        <Circle
          key={index}
          center={[flow.latitude, flow.longitude]}
          radius={100}
          pathOptions={{
            color: getColorForJamFactor(flow.jam_factor),
            fillColor: getColorForJamFactor(flow.jam_factor),
            fillOpacity: 0.7,
          }}
        >
          <Popup>
            <div>
              <p>Speed: {flow.speed} km/h</p>
              <p>Jam Factor: {flow.jam_factor}</p>
            </div>
          </Popup>
        </Circle>
      ))}
    </MapContainer>
  );
};

const getColorForJamFactor = (jamFactor) => {
  if (jamFactor <= 0.3) return "#00ff00"; // Green
  if (jamFactor <= 0.6) return "#ffff00"; // Yellow
  return "#ff0000"; // Red
};

export default TrafficMap;
