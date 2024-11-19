import React, { useState, useEffect } from "react";
import { trafficAPI } from "../services/api";
import TrafficMap from "./TrafficMap";
import PredictionChart from "./PredictionChart";

const Dashboard = () => {
  const [selectedCity, setSelectedCity] = useState("New York");
  const [incidents, setIncidents] = useState([]);
  const [trafficFlow, setTrafficFlow] = useState([]);
  const [loading, setLoading] = useState(false);

  const cities = ["New York", "Los Angeles", "Chicago"];

  useEffect(() => {
    fetchTrafficData();
  }, [selectedCity]);

  const fetchTrafficData = async () => {
    setLoading(true);
    try {
      const [incidentData, flowData] = await Promise.all([
        trafficAPI.getIncidents(selectedCity),
        trafficAPI.getTrafficFlow(selectedCity),
      ]);
      setIncidents(incidentData);
      setTrafficFlow(flowData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container p-4">
      <div className="header mb-4">
        <h1 className="text-2xl font-bold mb-4">Traffic Analytics Dashboard</h1>
        <select
          value={selectedCity}
          onChange={(e) => setSelectedCity(e.target.value)}
          className="p-2 border rounded"
        >
          {cities.map((city) => (
            <option key={city} value={city}>
              {city}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="loading-spinner">Loading...</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="map-container h-96 border rounded">
              <TrafficMap
                incidents={incidents}
                trafficFlow={trafficFlow}
                center={getCityCoordinates(selectedCity)}
              />
            </div>
            <div className="stats-container h-96 border rounded p-4">
              <PredictionChart data={trafficFlow} />
            </div>
          </div>
          <div className="incidents-list mt-4">
            <h2 className="text-xl font-semibold mb-2">Traffic Incidents</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {incidents.map((incident) => (
                <div
                  key={incident.id}
                  className="incident-card p-4 border rounded"
                >
                  <p className="font-semibold">{incident.type}</p>
                  <p className="text-sm">{incident.description}</p>
                  <p className="text-sm text-gray-500">
                    Severity: {incident.severity}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

const getCityCoordinates = (city) => {
  const coordinates = {
    "New York": [40.7128, -74.006],
    "Los Angeles": [34.0522, -118.2437],
    Chicago: [41.8781, -87.6298],
  };
  return coordinates[city] || coordinates["New York"];
};

export default Dashboard;
