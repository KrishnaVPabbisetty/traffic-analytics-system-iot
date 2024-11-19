import joblib
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor


class TrafficPredictor:
    def __init__(self):
        self.model = self._train_model()

    def _train_model(self):
        """Train a simple model with dummy data (for demonstration)"""
        # Generate dummy training data
        np.random.seed(42)
        X = np.random.rand(1000, 3)  # latitude, longitude, hour
        y = (
            0.3 * X[:, 0]
            + 0.5 * X[:, 1]
            + 0.2 * X[:, 2]
            + np.random.normal(0, 0.1, 1000)
        )

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model

    def predict(self, latitude: float, longitude: float, time: str):
        """Predict traffic conditions for given location and time"""
        try:
            # Parse time string to hour
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            hour = dt.hour / 24.0  # Normalize hour to 0-1 range

            # Make prediction
            features = np.array([[latitude, longitude, hour]])
            prediction = self.model.predict(features)[0]

            # Convert prediction to congestion level
            congestion_level = min(max(int(prediction * 10), 0), 10)

            return {
                "congestion_level": congestion_level,
                "description": self._get_congestion_description(congestion_level),
            }
        except Exception as e:
            return {
                "error": f"Prediction failed: {str(e)}",
                "congestion_level": 5,
                "description": "Unable to predict traffic conditions",
            }

    def _get_congestion_description(self, level: int) -> str:
        """Convert congestion level to human-readable description"""
        if level <= 3:
            return "Light traffic"
        elif level <= 6:
            return "Moderate traffic"
        else:
            return "Heavy traffic"
