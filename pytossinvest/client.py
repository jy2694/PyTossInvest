"""
Main Toss Invest API client.
"""

import time
from typing import Dict, Optional

import requests

from .api.account import AccountMixin
from .api.asset import AssetMixin
from .api.market_data import MarketDataMixin
from .api.market_info import MarketInfoMixin
from .api.order import OrderHistoryMixin, OrderInfoMixin, OrderMixin
from .api.stock_info import StockInfoMixin
from .errors import (
    APIError,
    AuthenticationError,
    InvalidCredentialsError,
    NetworkError,
    RateLimitExceededError,
    TokenExpiredError,
)
from .types import OAuth2TokenResponse


class TossInvestClient(
    MarketDataMixin,
    MarketInfoMixin,
    StockInfoMixin,
    AccountMixin,
    AssetMixin,
    OrderMixin,
    OrderHistoryMixin,
    OrderInfoMixin,
):
    """
    Client for Toss Investment Open API.

    This client handles authentication and provides methods to interact with
    the Toss Investment API endpoints.

    Args:
        client_id: OAuth2 Client ID
        client_secret: OAuth2 Client Secret
        base_url: Base URL for API endpoints (default: https://openapi.tossinvest.com)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = TossInvestClient(client_id="your_id", client_secret="your_secret")
        >>> client.authenticate()
        >>> # Now use the client to make API calls
    """

    BASE_URL = "https://openapi.tossinvest.com"
    TOKEN_ENDPOINT = "/oauth2/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = BASE_URL,
        timeout: int = 30,
    ):
        """Initialize the Toss Invest API client."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.timeout = timeout

        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0
        self._session = requests.Session()

    @property
    def access_token(self) -> Optional[str]:
        """Get the current access token."""
        return self._access_token

    @property
    def is_authenticated(self) -> bool:
        """Check if client is authenticated with valid token."""
        return self._access_token is not None and time.time() < self._token_expires_at

    def authenticate(self) -> OAuth2TokenResponse:
        """
        Authenticate using OAuth2 Client Credentials Grant.

        Exchanges client_id and client_secret for an access token.
        The token is stored internally and used for subsequent API requests.

        Returns:
            OAuth2TokenResponse: Token response containing access_token, token_type, expires_in

        Raises:
            InvalidCredentialsError: If client_id or client_secret are invalid
            AuthenticationError: If authentication fails for other reasons
            NetworkError: If network error occurs

        Example:
            >>> client = TossInvestClient(client_id="id", client_secret="secret")
            >>> token_response = client.authenticate()
            >>> print(token_response.access_token)
        """
        url = self.base_url + self.TOKEN_ENDPOINT

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "all",
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = self._session.post(
                url,
                data=payload,
                headers=headers,
                timeout=self.timeout,
            )

            # Handle OAuth2 standard error response
            if response.status_code != 200:
                error_data = response.json()
                error_code = error_data.get("error", "unknown_error")

                if error_code == "invalid_client":
                    raise InvalidCredentialsError(
                        "Invalid client credentials (client_id or client_secret)"
                    )
                elif error_code == "invalid_grant":
                    raise InvalidCredentialsError("Invalid grant type or credentials")
                else:
                    error_description = error_data.get("error_description", "Unknown error")
                    raise AuthenticationError(f"{error_code}: {error_description}")

            token_data = response.json()
            token_response = OAuth2TokenResponse.from_dict(token_data)

            # Store token and expiration time
            self._access_token = token_response.access_token
            self._token_expires_at = time.time() + token_response.expires_in - 60  # 60s buffer

            return token_response

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to authenticate: {str(e)}") from e
        except (ValueError, KeyError) as e:
            raise AuthenticationError(f"Invalid token response format: {str(e)}") from e

    def refresh_token(self) -> OAuth2TokenResponse:
        """
        Refresh the access token.

        Note: Toss API does not provide refresh_token, so this performs a full
        re-authentication using client credentials.

        Returns:
            OAuth2TokenResponse: New token response

        Raises:
            Same exceptions as authenticate()
        """
        return self.authenticate()

    def ensure_authenticated(self) -> None:
        """
        Ensure client is authenticated, raising error if not.

        Raises:
            AuthenticationError: If not authenticated or token expired
        """
        if not self.is_authenticated:
            raise AuthenticationError(
                "Not authenticated. Call authenticate() first or token has expired."
            )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        account_seq: Optional[int] = None,
    ) -> Dict:
        """
        Make HTTP request to API endpoint.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path (e.g., "/api/v1/accounts")
            params: Query parameters
            json: JSON body
            headers: Additional headers
            account_seq: Account sequence for X-Tossinvest-Account header

        Returns:
            Response data dictionary

        Raises:
            TokenExpiredError: If token has expired
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        self.ensure_authenticated()

        url = self.base_url + endpoint
        request_headers = self._build_headers(headers, account_seq)

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=request_headers,
                timeout=self.timeout,
            )

            # Extract request ID from response headers
            request_id = response.headers.get("X-Request-Id")

            # Handle API error responses
            if response.status_code >= 400:
                self._handle_error_response(response, request_id)

            return response.json()

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"API request failed: {str(e)}") from e

    def _build_headers(
        self, additional_headers: Optional[Dict] = None, account_seq: Optional[int] = None
    ) -> Dict:
        """Build request headers with authorization and account info."""
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        if account_seq is not None:
            headers["X-Tossinvest-Account"] = str(account_seq)

        if additional_headers:
            headers.update(additional_headers)

        return headers

    def _handle_error_response(
        self, response: requests.Response, request_id: Optional[str]
    ) -> None:
        """
        Handle API error response.

        Raises:
            TokenExpiredError: If token expired (401)
            RateLimitExceededError: If rate limit exceeded (429)
            APIError: For other API errors
        """
        try:
            error_data = response.json()
            error = error_data.get("error", {})
            code = error.get("code", "unknown_error")
            message = error.get("message", "Unknown error")
        except ValueError:
            code = f"http_{response.status_code}"
            message = response.text or response.reason

        if response.status_code == 401:
            if "token" in message.lower() or code == "invalid_token":
                raise TokenExpiredError(code, message, request_id)
            else:
                raise AuthenticationError(code, message, request_id)
        elif response.status_code == 429:
            raise RateLimitExceededError(code, message, request_id)
        else:
            raise APIError(code, message, request_id)

    def close(self) -> None:
        """Close the client session."""
        self._session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
