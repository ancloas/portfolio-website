import requests
from typing import Optional

class APIRequester:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.token = token

    def set_token(self, token: str):
        self.token = token

    def _headers(self, extra_headers=None):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = self._headers(kwargs.pop("headers", None))
        try:
            resp = requests.request(method, url, headers=headers, **kwargs)
            resp.raise_for_status()
            if resp.content:
                return resp.json()
            return {}
        except requests.RequestException as e:
            return {"error": str(e), "response": getattr(e, 'response', None)}