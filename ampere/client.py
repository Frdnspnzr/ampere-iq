"""
Main API client implementation.
"""

import requests
from types import SimpleNamespace


class AmpereClient:
    """
    API client for accessing the Ampere API.

    Args:
        base_url: The base URL for the API

    Example:
        >>> client = AmpereClient('https://api.example.com')
        >>> # Use client methods here (to be implemented)
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self._session = requests.Session()

    def login(self, password: str) -> None:
        """
        Authenticate with the API using a password.

        Args:
            password: The password for authentication

        Raises:
            requests.exceptions.RequestException: If the login request fails
        """
        url = f"{self.base_url}/auth/login"
        form_data = {
            'username': 'installer',
            'url': '/',
            'submit': 'Login',
            'password': password
        }

        response = self._session.post(url, data=form_data, allow_redirects=False)

        # Expect a 303 redirect with Set-Cookie header
        if response.status_code != 303:
            raise requests.exceptions.HTTPError(
                f"Login failed with status code {response.status_code}"
            )

        # Verify we received the session cookie
        if 'kiwisessionid' not in self._session.cookies:
            raise requests.exceptions.HTTPError(
                "Login failed: kiwisessionid cookie not received"
            )

    def energy_overview(self) -> SimpleNamespace:
        """
        Fetch energy overview data from the API.

        Returns:
            SimpleNamespace: Energy overview data with attribute access

        Raises:
            requests.exceptions.RequestException: If the request fails

        Example:
            >>> overview = client.energy_overview()
            >>> print(overview.production)
        """
        url = f"{self.base_url}/rest/hems-configurator/energy-overview"
        response = self._session.get(url)
        response.raise_for_status()

        data = response.json()
        return self._dict_to_namespace(data)

    def _dict_to_namespace(self, data):
        """
        Recursively convert a dictionary to a SimpleNamespace for attribute access.

        Args:
            data: Dictionary or other data to convert

        Returns:
            SimpleNamespace if dict, list of SimpleNamespace if list, otherwise original data
        """
        if isinstance(data, dict):
            return SimpleNamespace(**{k: self._dict_to_namespace(v) for k, v in data.items()})
        elif isinstance(data, list):
            return [self._dict_to_namespace(item) for item in data]
        else:
            return data

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
