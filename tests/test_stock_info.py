"""Tests for Stock Info API."""

import pytest
from unittest.mock import patch

from pytossinvest import TossInvestClient
from pytossinvest.types import StockInfo, StockWarning, KrMarketDetail


class TestStockInfoAPI:
    """Test Stock Info API methods."""

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

    def test_get_stocks_single(self, authenticated_client):
        """Test get_stocks with single symbol."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "005930",
                    "stockName": "삼성전자",
                    "market": "KR",
                    "currency": "KRW",
                    "listingDate": "1975-06-10",
                    "listingStatus": "NORMAL",
                    "tradingSuspended": False,
                    "sharesOutstanding": 5969782550,
                    "krMarketDetail": {
                        "krxTradingSuspended": False,
                        "nxtTradingSuspended": False,
                    },
                }
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stocks(["005930"])

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], StockInfo)
            assert result[0].symbol == "005930"
            assert result[0].stockName == "삼성전자"
            assert result[0].market == "KR"
            assert result[0].currency == "KRW"
            assert result[0].tradingSuspended is False
            assert isinstance(result[0].krMarketDetail, KrMarketDetail)

    def test_get_stocks_multiple(self, authenticated_client):
        """Test get_stocks with multiple symbols."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "005930",
                    "stockName": "삼성전자",
                    "market": "KR",
                    "currency": "KRW",
                    "listingDate": "1975-06-10",
                    "listingStatus": "NORMAL",
                    "tradingSuspended": False,
                    "sharesOutstanding": 5969782550,
                    "krMarketDetail": {
                        "krxTradingSuspended": False,
                        "nxtTradingSuspended": False,
                    },
                },
                {
                    "symbol": "000660",
                    "stockName": "SK하이닉스",
                    "market": "KR",
                    "currency": "KRW",
                    "listingDate": "1995-12-29",
                    "listingStatus": "NORMAL",
                    "tradingSuspended": False,
                    "sharesOutstanding": 748696924,
                    "krMarketDetail": {
                        "krxTradingSuspended": False,
                        "nxtTradingSuspended": False,
                    },
                },
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stocks(["005930", "000660"])

            assert len(result) == 2
            assert all(isinstance(s, StockInfo) for s in result)
            assert result[0].symbol == "005930"
            assert result[1].symbol == "000660"

    def test_get_stocks_us_symbol(self, authenticated_client):
        """Test get_stocks with US symbol."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "AAPL",
                    "stockName": "Apple Inc.",
                    "market": "US",
                    "currency": "USD",
                    "listingDate": "1980-12-12",
                    "listingStatus": "NORMAL",
                    "tradingSuspended": False,
                    "sharesOutstanding": 15600000000,
                    "krMarketDetail": None,
                }
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stocks(["AAPL"])

            assert len(result) == 1
            assert result[0].symbol == "AAPL"
            assert result[0].market == "US"
            assert result[0].currency == "USD"
            assert result[0].krMarketDetail is None

    def test_get_stocks_limit_exceeded(self, authenticated_client):
        """Test get_stocks raises error when exceeding 200 symbol limit."""
        with pytest.raises(ValueError, match="Maximum 200 symbols allowed"):
            authenticated_client.get_stocks(["SYMBOL"] * 201)

    def test_get_stock_warnings_with_warnings(self, authenticated_client):
        """Test get_stock_warnings returns active warnings."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "005930",
                    "warningType": "INVESTMENT_WARNING",
                    "startDate": "2024-01-10",
                    "endDate": None,
                    "exchange": "KRX",
                },
                {
                    "symbol": "005930",
                    "warningType": "VI_STATIC",
                    "startDate": "2024-01-08",
                    "endDate": "2024-01-09",
                    "exchange": "KRX",
                },
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stock_warnings("005930")

            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(w, StockWarning) for w in result)
            assert result[0].warningType == "INVESTMENT_WARNING"
            assert result[0].endDate is None
            assert result[1].warningType == "VI_STATIC"
            assert result[1].endDate == "2024-01-09"

    def test_get_stock_warnings_no_warnings(self, authenticated_client):
        """Test get_stock_warnings returns empty list when no warnings."""
        mock_response_data = {"result": []}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stock_warnings("005930")

            assert isinstance(result, list)
            assert len(result) == 0

    def test_get_stock_warnings_various_types(self, authenticated_client):
        """Test get_stock_warnings with various warning types."""
        warning_types = [
            "LIQUIDATION_TRADING",
            "OVERHEATED",
            "INVESTMENT_WARNING",
            "INVESTMENT_RISK",
            "VI_STATIC",
            "VI_DYNAMIC",
            "VI_STATIC_AND_DYNAMIC",
            "STOCK_WARRANTS",
        ]

        mock_result = [
            {
                "symbol": "005930",
                "warningType": wtype,
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
                "exchange": "KRX",
            }
            for wtype in warning_types
        ]

        mock_response_data = {"result": mock_result}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stock_warnings("005930")

            assert len(result) == len(warning_types)
            for i, wtype in enumerate(warning_types):
                assert result[i].warningType == wtype

    def test_get_stock_warnings_us_exchange(self, authenticated_client):
        """Test get_stock_warnings with US exchange."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "AAPL",
                    "warningType": "INVESTMENT_WARNING",
                    "startDate": "2024-01-15",
                    "endDate": None,
                    "exchange": "NASDAQ",
                }
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_stock_warnings("AAPL")

            assert len(result) == 1
            assert result[0].exchange == "NASDAQ"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
