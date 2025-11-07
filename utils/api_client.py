

class ApiClient:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json",
        }
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def get(self, endpoint, params=None):
        import requests

        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        import requests
        import json

        url = f"{self.base_url}{endpoint}"
        response = requests.post(
            url, headers=self._get_headers(), data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        import requests
        import json

        url = f"{self.base_url}{endpoint}"
        response = requests.put(
            url, headers=self._get_headers(), data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        import requests

        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.status_code == 204