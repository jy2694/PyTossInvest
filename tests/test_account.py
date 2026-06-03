"""Tests for Account API."""

import pytest
from unittest.mock import patch

from py_toss_invest import TossInvestClient
from py_toss_invest.types import Account


class TestAccountAPI:
    """Test Account API methods."""

    @pytest.fixture
    def authenticated_client(self):
        """Create authenticated client for testing."""
        client = TossInvestClient(
            client_id="test_id",
            client_secret="test_secret",
        )
        # Manually set token to simulate authenticated state
        client._access_token = "test_token"
        client._token_expires_at = float("inf")
        return client

    def test_get_accounts_single(self, authenticated_client):
        """Test get_accounts with single account."""
        mock_response_data = {
            "result": [
                {
                    "accountSeq": 12345,
                    "accountName": "일반투자계좌",
                    "accountType": "BROKERAGE",
                    "status": "NORMAL",
                    "nickname": "메인계좌",
                }
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_accounts()

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], Account)
            assert result[0].accountSeq == 12345
            assert result[0].accountName == "일반투자계좌"
            assert result[0].accountType == "BROKERAGE"
            assert result[0].status == "NORMAL"
            assert result[0].nickname == "메인계좌"

    def test_get_accounts_multiple(self, authenticated_client):
        """Test get_accounts with multiple accounts."""
        mock_response_data = {
            "result": [
                {
                    "accountSeq": 12345,
                    "accountName": "일반투자계좌",
                    "accountType": "BROKERAGE",
                    "status": "NORMAL",
                    "nickname": "메인계좌",
                },
                {
                    "accountSeq": 67890,
                    "accountName": "연금저축",
                    "accountType": "PENSION_SAVINGS",
                    "status": "NORMAL",
                    "nickname": None,
                },
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_accounts()

            assert len(result) == 2
            assert all(isinstance(a, Account) for a in result)
            assert result[0].accountSeq == 12345
            assert result[1].accountSeq == 67890
            assert result[0].accountType == "BROKERAGE"
            assert result[1].accountType == "PENSION_SAVINGS"

    def test_get_accounts_empty(self, authenticated_client):
        """Test get_accounts returns empty list when user has no accounts."""
        mock_response_data = {"result": []}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_accounts()

            assert isinstance(result, list)
            assert len(result) == 0

    def test_get_accounts_various_types(self, authenticated_client):
        """Test get_accounts with various account types."""
        account_types = [
            "BROKERAGE",
            "OVERSEAS_DERIVATIVES",
            "PENSION_SAVINGS",
            "RESHORING_INVESTMENT",
        ]

        mock_result = [
            {
                "accountSeq": 10000 + i,
                "accountName": f"계좌{i}",
                "accountType": atype,
                "status": "NORMAL",
                "nickname": None,
            }
            for i, atype in enumerate(account_types)
        ]

        mock_response_data = {"result": mock_result}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_accounts()

            assert len(result) == len(account_types)
            for i, atype in enumerate(account_types):
                assert result[i].accountType == atype

    def test_get_accounts_correct_endpoint(self, authenticated_client):
        """Test get_accounts calls correct endpoint."""
        mock_response_data = {"result": []}

        with patch.object(
            authenticated_client, "_make_request", return_value=mock_response_data
        ) as mock_make_request:
            authenticated_client.get_accounts()

            # Verify correct endpoint is called
            mock_make_request.assert_called_once()
            call_kwargs = mock_make_request.call_args[1]
            assert call_kwargs["method"] == "GET"
            assert call_kwargs["endpoint"] == "/api/v1/accounts"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
