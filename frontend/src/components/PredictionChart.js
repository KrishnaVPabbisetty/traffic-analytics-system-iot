import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const PredictionChart = ({ data }) => {
  // Process data for the chart
  const chartData = data.map((item) => ({
    time: new Date(item.timestamp).toLocaleTimeString(),
    speed: item.speed,
    jamFactor: item.jam_factor * 10, // Scale up jam factor for better visualization
  }));

  return (
    <div className="h-full">
      <h3 className="text-lg font-semibold mb-4">Traffic Flow Analysis</h3>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            tick={{ fontSize: 12 }}
            interval={Math.floor(chartData.length / 5)}
          />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="speed"
            stroke="#8884d8"
            name="Speed (km/h)"
          />
          <Line
            type="monotone"
            dataKey="jamFactor"
            stroke="#82ca9d"
            name="Congestion Level"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionChart;
