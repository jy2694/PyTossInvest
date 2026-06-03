"""Tests for Market Data API."""

import pytest
from unittest.mock import patch

from pytossinvest import TossInvestClient
from pytossinvest.types import (
    OrderbookResponse,
    PriceResponse,
    TradeResponse,
    PriceLimitResponse,
    CandlePageResponse,
)


class TestMarketDataAPI:
    """Test Market Data API methods."""

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

    def test_get_orderbook(self, authenticated_client):
        """Test get_orderbook method."""
        mock_response_data = {
            "result": {
                "symbol": "005930",
                "asks": [
                    {"price": 70000, "volume": 100},
                    {"price": 70100, "volume": 50},
                ],
                "bids": [
                    {"price": 69900, "volume": 200},
                    {"price": 69800, "volume": 150},
                ],
                "timestamp": "2024-01-01T09:00:00Z",
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_orderbook("005930")

            assert isinstance(result, OrderbookResponse)
            assert result.symbol == "005930"
            assert len(result.asks) == 2
            assert len(result.bids) == 2
            assert result.asks[0].price == 70000
            assert result.bids[0].price == 69900

    def test_get_prices_single(self, authenticated_client):
        """Test get_prices with single symbol."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "005930",
                    "currentPrice": 70000,
                    "highPrice": 71000,
                    "lowPrice": 69000,
                    "openPrice": 69500,
                    "closePrice": 70000,
                    "previousClosePrice": 69800,
                    "timestamp": "2024-01-01T09:00:00Z",
                    "currency": "KRW",
                }
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_prices(["005930"])

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], PriceResponse)
            assert result[0].symbol == "005930"
            assert result[0].currentPrice == 70000
            assert result[0].currency == "KRW"

    def test_get_prices_multiple(self, authenticated_client):
        """Test get_prices with multiple symbols."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "005930",
                    "currentPrice": 70000,
                    "highPrice": 71000,
                    "lowPrice": 69000,
                    "openPrice": 69500,
                    "closePrice": 70000,
                    "previousClosePrice": 69800,
                    "timestamp": "2024-01-01T09:00:00Z",
                    "currency": "KRW",
                },
                {
                    "symbol": "000660",
                    "currentPrice": 100000,
                    "highPrice": 101000,
                    "lowPrice": 99000,
                    "openPrice": 99500,
                    "closePrice": 100000,
                    "previousClosePrice": 99800,
                    "timestamp": "2024-01-01T09:00:00Z",
                    "currency": "KRW",
                },
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_prices(["005930", "000660"])

            assert len(result) == 2
            assert all(isinstance(p, PriceResponse) for p in result)

    def test_get_prices_limit_exceeded(self, authenticated_client):
        """Test get_prices raises error when exceeding 200 symbol limit."""
        with pytest.raises(ValueError, match="Maximum 200 symbols allowed"):
            authenticated_client.get_prices(["SYMBOL"] * 201)

    def test_get_trades(self, authenticated_client):
        """Test get_trades method."""
        mock_response_data = {
            "result": {
                "symbol": "005930",
                "timestamp": "2024-01-01T09:00:00Z",
                "trades": [
                    {
                        "price": 70000,
                        "quantity": 100,
                        "timestamp": "2024-01-01T08:59:00Z",
                        "side": "BUY",
                        "currency": "KRW",
                    },
                    {
                        "price": 70100,
                        "quantity": 50,
                        "timestamp": "2024-01-01T08:58:00Z",
                        "side": "SELL",
                        "currency": "KRW",
                    },
                ],
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_trades("005930")

            assert isinstance(result, TradeResponse)
            assert result.symbol == "005930"
            assert len(result.trades) == 2
            assert result.trades[0].side == "BUY"
            assert result.trades[1].side == "SELL"

    def test_get_price_limits(self, authenticated_client):
        """Test get_price_limits method."""
        mock_response_data = {
            "result": [
                {
                    "symbol": "005930",
                    "highLimitPrice": 80000,
                    "lowLimitPrice": 60000,
                    "currency": "KRW",
                }
            ]
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_price_limits(["005930"])

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], PriceLimitResponse)
            assert result[0].highLimitPrice == 80000
            assert result[0].lowLimitPrice == 60000

    def test_get_price_limits_limit_exceeded(self, authenticated_client):
        """Test get_price_limits raises error when exceeding 200 symbol limit."""
        with pytest.raises(ValueError, match="Maximum 200 symbols allowed"):
            authenticated_client.get_price_limits(["SYMBOL"] * 201)

    def test_get_candles(self, authenticated_client):
        """Test get_candles method."""
        mock_response_data = {
            "result": {
                "symbol": "005930",
                "period": "1d",
                "candles": [
                    {
                        "candleDateTime": "2024-01-01T00:00:00Z",
                        "openPrice": 69500,
                        "highPrice": 71000,
                        "lowPrice": 69000,
                        "closePrice": 70000,
                        "volume": 10000,
                        "currency": "KRW",
                    },
                    {
                        "candleDateTime": "2023-12-31T00:00:00Z",
                        "openPrice": 69000,
                        "highPrice": 70000,
                        "lowPrice": 68000,
                        "closePrice": 69500,
                        "volume": 9000,
                        "currency": "KRW",
                    },
                ],
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_candles("005930", period="1d", count=2)

            assert isinstance(result, CandlePageResponse)
            assert result.symbol == "005930"
            assert result.period == "1d"
            assert len(result.candles) == 2
            assert result.candles[0].closePrice == 70000

    def test_get_candles_limit_exceeded(self, authenticated_client):
        """Test get_candles raises error when exceeding 200 candle limit."""
        with pytest.raises(ValueError, match="Maximum 200 candles allowed"):
            authenticated_client.get_candles("005930", count=201)

    def test_get_candles_default_period(self, authenticated_client):
        """Test get_candles uses default period of 1d."""
        mock_response_data = {"result": {"symbol": "005930", "period": "1d", "candles": []}}

        with patch.object(
            authenticated_client, "_make_request", return_value=mock_response_data
        ) as mock_make_request:
            authenticated_client.get_candles("005930")

            # Verify that period defaults to 1d
            mock_make_request.assert_called_once()
            call_kwargs = mock_make_request.call_args[1]
            assert call_kwargs["params"]["period"] == "1d"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
