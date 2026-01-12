"""Auto-generated API Client"""

import requests
from typing import Dict, Any


class APIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def get(self, endpoint: str) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/{endpoint}", json=data, headers=self.headers
        )
        response.raise_for_status()
        return response.json()
