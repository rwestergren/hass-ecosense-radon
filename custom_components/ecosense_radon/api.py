"""API for EcoSense Radon."""

from __future__ import annotations

import requests
from botocore import UNSIGNED
from botocore.client import Config
from pycognito import Cognito

from .const import (
    API_URL,
    CLIENT_ID,
    USER_POOL_ID,
    USER_POOL_REGION,
)


class EcoSenseApiClient:
    """A client to communicate with the EcoSense API."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the API client."""
        self._username = username
        self._password = password
        self._cognito: Cognito | None = None

    @property
    def cognito(self) -> Cognito:
        """Get or create the Cognito object."""
        if self._cognito is None:
            self._cognito = Cognito(
                USER_POOL_ID,
                CLIENT_ID,
                user_pool_region=USER_POOL_REGION,
                username=self._username,
                boto3_client_kwargs={"config": Config(signature_version=UNSIGNED)},
            )
        return self._cognito

    def authenticate(self) -> bool:
        """Authenticate with EcoSense Cognito and get an ID token."""
        self.cognito.authenticate(password=self._password)
        return True

    def _make_request(self) -> list:
        """Make the API request to get devices."""
        id_token = self.cognito.id_token
        headers = {"Authorization": f"Bearer {id_token}"}
        params = {"email": self._username}
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_devices(self) -> list:
        """Get devices from EcoSense API."""
        try:
            return self._make_request()
        except requests.exceptions.HTTPError as err:
            if err.response is not None and err.response.status_code == 401:
                # Token likely expired, re-authenticate and try again.
                self.authenticate()
                return self._make_request()
            # Re-raise other HTTP errors.
            raise
        except Exception:
            # Broad exception to catch any token refresh errors from pycognito.
            # Re-authenticate and try again.
            self.authenticate()
            return self._make_request()
