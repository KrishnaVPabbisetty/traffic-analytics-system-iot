import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "Traffic Analytics System"
    PROJECT_VERSION = "1.0.0"

    # HERE Maps API credentials - Sign up at https://developer.here.com/
    HERE_API_KEY = os.getenv(
        "HERE_API_KEY", "YzvGEMt1vRb3WUhMS0AvRXgTNjHwbOme5zK31I2smK4"
    )

    if not HERE_API_KEY:
        raise ValueError(
            "HERE_API_KEY is not set. Please define it in your .env file or as an environment variable."
        )

    # Example cities for traffic data
    MONITORED_CITIES = [
        {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
        {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437},
        {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    ]


settings = Settings()
