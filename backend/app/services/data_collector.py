import requests
from datetime import datetime
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class TrafficDataCollector:
    def __init__(self):
        self.api_key = settings.HERE_API_KEY
        self.base_url = "https://traffic.ls.hereapi.com/traffic/6.2"

    async def get_traffic_incidents(
        self, latitude: float, longitude: float, radius: int = 1000
    ):
        """Fetch traffic incidents from HERE Maps API"""
        try:
            params = {
                "apiKey": self.api_key,
                "prox": f"{latitude},{longitude},{radius}",
                "responseattributes": "sh,fc",
                "format": "json",
            }

            response = requests.get(f"{self.base_url}/incidents.json", params=params)
            response.raise_for_status()

            data = response.json()
            return self._parse_incidents(data)

        except Exception as e:
            logger.error(f"Error fetching traffic incidents: {str(e)}")
            return []

    async def get_traffic_flow(
        self, latitude: float, longitude: float, radius: int = 1000
    ):
        """Fetch traffic flow data from HERE Maps API"""
        try:
            params = {
                "apiKey": self.api_key,
                "prox": f"{latitude},{longitude},{radius}",
                "responseattributes": "sh,fc",
                "format": "json",
            }

            response = requests.get(f"{self.base_url}/flow.json", params=params)
            response.raise_for_status()

            data = response.json()
            return self._parse_flow(data)

        except Exception as e:
            logger.error(f"Error fetching traffic flow: {str(e)}")
            return []

    def _parse_incidents(self, data):
        incidents = []
        try:
            for item in data.get("TRAFFIC_ITEMS", {}).get("TRAFFIC_ITEM", []):
                incident = {
                    "id": item.get("TRAFFIC_ITEM_ID"),
                    "type": item.get("TRAFFIC_ITEM_TYPE_DESC"),
                    "severity": item.get("CRITICALITY", {}).get("ID", 0),
                    "start_time": datetime.fromtimestamp(item.get("START_TIME") / 1000),
                    "latitude": item.get("LOCATION", {})
                    .get("GEOLOC", {})
                    .get("LATITUDE"),
                    "longitude": item.get("LOCATION", {})
                    .get("GEOLOC", {})
                    .get("LONGITUDE"),
                    "description": item.get("TRAFFIC_ITEM_DESCRIPTION", [{}])[0].get(
                        "value"
                    ),
                }
                incidents.append(incident)
        except Exception as e:
            logger.error(f"Error parsing incidents: {str(e)}")
        return incidents

    def _parse_flow(self, data):
        flow_data = []
        try:
            for item in data.get("RWS", []):
                for road in item.get("RW", []):
                    flow = {
                        "latitude": road.get("FIS")[0]
                        .get("FI")[0]
                        .get("TMC", {})
                        .get("PC"),
                        "longitude": road.get("FIS")[0]
                        .get("FI")[0]
                        .get("TMC", {})
                        .get("QD"),
                        "speed": road.get("FIS")[0].get("FI")[0].get("CF")[0].get("SP"),
                        "jam_factor": road.get("FIS")[0]
                        .get("FI")[0]
                        .get("CF")[0]
                        .get("JF"),
                        "timestamp": datetime.now(),
                    }
                    flow_data.append(flow)
        except Exception as e:
            logger.error(f"Error parsing flow data: {str(e)}")
        return flow_data
