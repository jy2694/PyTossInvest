"""Tests for Asset, Order, Order History, and Order Info APIs (Phases 5-8)."""

import pytest
from unittest.mock import patch

from pytossinvest import (
    TossInvestClient,
    BuyingPowerResponse,
    CommissionsResponse,
    HoldingsOverview,
    Order,
    OrderOperationResponse,
    OrderResponse,
    PaginatedOrderResponse,
    SellableQuantityResponse,
)


class TestAssetAPI:
    """Test Asset API methods (Phase 5)."""

    @pytest.fixture
    def authenticated_client(self):
        client = TossInvestClient(client_id="test_id", client_secret="test_secret")
        client._access_token = "test_token"
        client._token_expires_at = float("inf")
        return client

    def test_get_holdings(self, authenticated_client):
        """Test get_holdings method."""
        mock_response_data = {
            "result": {
                "items": [
                    {
                        "symbol": "005930",
                        "quantity": 10,
                        "currency": "KRW",
                        "cost": {"krw": 700000},
                        "marketValue": {"amount": 750000, "amountAfterCost": 750000},
                        "profitLoss": {"amount": 50000, "rate": 0.071, "rateAfterCost": 0.071},
                        "dailyProfitLoss": {"amount": 10000, "rate": 0.01},
                        "costPrice": 70000,
                        "currentPrice": 75000,
                    }
                ],
                "summary": {"totalValue": 750000},
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_holdings(12345)

            assert isinstance(result, HoldingsOverview)
            assert len(result.items) == 1
            assert result.items[0].symbol == "005930"
            assert result.items[0].quantity == 10


class TestOrderAPI:
    """Test Order API methods (Phase 6)."""

    @pytest.fixture
    def authenticated_client(self):
        client = TossInvestClient(client_id="test_id", client_secret="test_secret")
        client._access_token = "test_token"
        client._token_expires_at = float("inf")
        return client

    def test_create_order(self, authenticated_client):
        """Test create_order method."""
        mock_response_data = {"result": {"orderId": "order_12345"}}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.create_order(
                account_seq=12345,
                symbol="005930",
                side="BUY",
                quantity=10,
                order_type="LIMIT",
                price=70000,
            )

            assert isinstance(result, OrderResponse)
            assert result.orderId == "order_12345"

    def test_modify_order(self, authenticated_client):
        """Test modify_order method."""
        mock_response_data = {"result": {"orderId": "order_12345"}}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.modify_order(
                account_seq=12345,
                order_id="order_12345",
                order_type="LIMIT",
                price=71000,
            )

            assert isinstance(result, OrderOperationResponse)
            assert result.orderId == "order_12345"

    def test_cancel_order(self, authenticated_client):
        """Test cancel_order method."""
        mock_response_data = {"result": {"orderId": "order_12345"}}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.cancel_order(account_seq=12345, order_id="order_12345")

            assert isinstance(result, OrderOperationResponse)
            assert result.orderId == "order_12345"


class TestOrderHistoryAPI:
    """Test Order History API methods (Phase 7)."""

    @pytest.fixture
    def authenticated_client(self):
        client = TossInvestClient(client_id="test_id", client_secret="test_secret")
        client._access_token = "test_token"
        client._token_expires_at = float("inf")
        return client

    def test_get_orders(self, authenticated_client):
        """Test get_orders method."""
        mock_response_data = {
            "result": {
                "orders": [
                    {
                        "orderId": "order_12345",
                        "symbol": "005930",
                        "orderType": "LIMIT",
                        "side": "BUY",
                        "quantity": 10,
                        "price": 70000,
                        "status": "PENDING",
                        "execution": {
                            "status": "PENDING",
                            "filledQuantity": 0,
                            "orderedAt": "2024-01-01T09:00:00Z",
                        },
                    }
                ],
                "nextCursor": None,
                "hasNext": False,
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_orders(12345, status="OPEN")

            assert isinstance(result, PaginatedOrderResponse)
            assert len(result.orders) == 1
            assert result.orders[0].symbol == "005930"
            assert result.hasNext is False

    def test_get_order(self, authenticated_client):
        """Test get_order method."""
        mock_response_data = {
            "result": {
                "orderId": "order_12345",
                "symbol": "005930",
                "orderType": "LIMIT",
                "side": "BUY",
                "quantity": 10,
                "price": 70000,
                "status": "FILLED",
                "execution": {
                    "status": "FILLED",
                    "filledQuantity": 10,
                    "filledPrice": 70000,
                    "orderedAt": "2024-01-01T09:00:00Z",
                    "filledAt": "2024-01-01T09:01:00Z",
                    "settlementDate": "2024-01-03",
                },
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_order(12345, "order_12345")

            assert isinstance(result, Order)
            assert result.orderId == "order_12345"
            assert result.status == "FILLED"


class TestOrderInfoAPI:
    """Test Order Info API methods (Phase 8)."""

    @pytest.fixture
    def authenticated_client(self):
        client = TossInvestClient(client_id="test_id", client_secret="test_secret")
        client._access_token = "test_token"
        client._token_expires_at = float("inf")
        return client

    def test_get_buying_power(self, authenticated_client):
        """Test get_buying_power method."""
        mock_response_data = {
            "result": {
                "cashBuyingPower": 1000000,
                "subscriptionBuyingPower": None,
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_buying_power(12345)

            assert isinstance(result, BuyingPowerResponse)
            assert result.cashBuyingPower == 1000000

    def test_get_sellable_quantity(self, authenticated_client):
        """Test get_sellable_quantity method."""
        mock_response_data = {"result": {"sellableQuantity": 10}}

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_sellable_quantity(12345, "005930")

            assert isinstance(result, SellableQuantityResponse)
            assert result.sellableQuantity == 10

    def test_get_commissions(self, authenticated_client):
        """Test get_commissions method."""
        mock_response_data = {
            "result": {
                "commissions": [
                    {"market": "KR", "commissionRate": 0.0015},
                    {"market": "US", "commissionRate": 0.001},
                ]
            }
        }

        with patch.object(authenticated_client, "_make_request", return_value=mock_response_data):
            result = authenticated_client.get_commissions(12345)

            assert isinstance(result, CommissionsResponse)
            assert len(result.commissions) == 2
            assert result.commissions[0].market == "KR"
            assert result.commissions[0].commissionRate == 0.0015


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
