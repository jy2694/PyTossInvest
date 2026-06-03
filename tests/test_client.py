"""Tests for TossInvestClient."""

import pytest
from unittest.mock import patch, MagicMock

from py_toss_invest import TossInvestClient
from py_toss_invest.errors import (
    InvalidCredentialsError,
    AuthenticationError,
    NetworkError,
)


class TestTossInvestClient:
    """Test TossInvestClient initialization and authentication."""

    def test_client_initialization(self):
        """Test client can be initialized with credentials."""
        client = TossInvestClient(
            client_id="test_id",
            client_secret="test_secret",
        )
        assert client.client_id == "test_id"
        assert client.client_secret == "test_secret"
        assert not client.is_authenticated

    def test_authenticate_success(self):
        """Test successful authentication."""
        client = TossInvestClient(
            client_id="test_id",
            client_secret="test_secret",
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_token_abc123",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "all",
        }

        with patch.object(client._session, "post", return_value=mock_response):
            token_response = client.authenticate()

            assert token_response.access_token == "test_token_abc123"
            assert token_response.token_type == "Bearer"
            assert token_response.expires_in == 3600
            assert client.is_authenticated
            assert client.access_token == "test_token_abc123"

    def test_authenticate_invalid_credentials(self):
        """Test authentication with invalid credentials."""
        client = TossInvestClient(
            client_id="invalid_id",
            client_secret="invalid_secret",
        )

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "invalid_client",
            "error_description": "Client authentication failed",
        }

        with patch.object(client._session, "post", return_value=mock_response):
            with pytest.raises(InvalidCredentialsError):
                client.authenticate()

    def test_authenticate_network_error(self):
        """Test authentication with network error."""
        import requests

        client = TossInvestClient(
            client_id="test_id",
            client_secret="test_secret",
        )

        with patch.object(
            client._session,
            "post",
            side_effect=requests.exceptions.ConnectionError("Connection failed"),
        ):
            with pytest.raises(NetworkError):
                client.authenticate()

    def test_ensure_authenticated_raises_when_not_authenticated(self):
        """Test ensure_authenticated raises error when not authenticated."""
        client = TossInvestClient(
            client_id="test_id",
            client_secret="test_secret",
        )

        with pytest.raises(AuthenticationError):
            client.ensure_authenticated()

    def test_context_manager(self):
        """Test client works as context manager."""
        with TossInvestClient(
            client_id="test_id",
            client_secret="test_secret",
        ) as client:
            assert client is not None
            assert client.client_id == "test_id"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
