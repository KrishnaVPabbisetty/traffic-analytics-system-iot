import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const trafficAPI = {
  async getIncidents(city) {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/traffic/incidents/${city}`
      );
      return response.data.incidents;
    } catch (error) {
      console.error("Error fetching incidents:", error);
      return [];
    }
  },

  async getTrafficFlow(city) {
    try {
      const response = await axios.get(`${API_BASE_URL}/traffic/flow/${city}`);
      return response.data.flow_data;
    } catch (error) {
      console.error("Error fetching traffic flow:", error);
      return [];
    }
  },

  async predictTraffic(latitude, longitude, time) {
    try {
      const response = await axios.post(`${API_BASE_URL}/traffic/predict`, {
        latitude,
        longitude,
        time,
      });
      return response.data.prediction;
    } catch (error) {
      console.error("Error getting prediction:", error);
      return null;
    }
  },
};
