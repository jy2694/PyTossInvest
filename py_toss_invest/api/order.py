"""Order, Order History, and Order Info API methods for TossInvestClient."""

from typing import List, Optional

from py_toss_invest.types import (
    BuyingPowerResponse,
    Commission,
    Order,
    OrderOperationResponse,
    OrderResponse,
    PaginatedOrderResponse,
    SellableQuantityResponse,
)


class OrderMixin:
    """Mixin providing Order API methods (create, modify, cancel)."""

    def create_order(
        self,
        account_seq: int,
        symbol: str,
        side: str,
        order_type: str = "LIMIT",
        quantity: Optional[str] = None,
        price: Optional[str] = None,
        order_amount: Optional[str] = None,
        time_in_force: Optional[str] = None,
        client_order_id: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderResponse:
        """
        Create a new order.

        Args:
            account_seq: Account sequence number
            symbol: Stock symbol
            side: BUY or SELL
            order_type: LIMIT or MARKET (default: LIMIT)
            quantity: Order quantity as string (required for quantity-based orders)
            price: Limit price as string (required for LIMIT orders)
            order_amount: Order amount in USD as string (US MARKET only, MARKET orders only)
            time_in_force: DAY or CLS (default: DAY). CLS only for US LIMIT orders.
            client_order_id: Idempotency key (max 36 chars, alphanumeric/-/_)
            confirm_high_value_order: Required true for orders >= 100M KRW

        Returns:
            OrderResponse: Created order with orderId
        """
        request_body = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
        }

        if quantity is not None:
            request_body["quantity"] = quantity
        if price is not None:
            request_body["price"] = price
        if order_amount is not None:
            request_body["orderAmount"] = order_amount
        if time_in_force is not None:
            request_body["timeInForce"] = time_in_force
        if client_order_id is not None:
            request_body["clientOrderId"] = client_order_id
        if confirm_high_value_order:
            request_body["confirmHighValueOrder"] = confirm_high_value_order

        response_data = self._make_request(
            method="POST",
            endpoint="/api/v1/orders",
            json=request_body,
            account_seq=account_seq,
        )
        return OrderResponse.from_dict(response_data.get("result", {}))

    def modify_order(
        self,
        account_seq: int,
        order_id: str,
        order_type: str,
        price: Optional[str] = None,
        quantity: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderOperationResponse:
        """
        Modify an existing order.

        Args:
            account_seq: Account sequence number
            order_id: Order ID to modify
            order_type: Order type (LIMIT or MARKET)
            price: New price as string (for LIMIT orders)
            quantity: New quantity as string (KR market only)
            confirm_high_value_order: Required true for orders >= 100M KRW

        Returns:
            OrderOperationResponse
        """
        request_body = {"orderType": order_type}

        if price is not None:
            request_body["price"] = price
        if quantity is not None:
            request_body["quantity"] = quantity
        if confirm_high_value_order:
            request_body["confirmHighValueOrder"] = confirm_high_value_order

        response_data = self._make_request(
            method="POST",
            endpoint=f"/api/v1/orders/{order_id}/modify",
            json=request_body,
            account_seq=account_seq,
        )
        return OrderOperationResponse.from_dict(response_data.get("result", {}))

    def cancel_order(self, account_seq: int, order_id: str) -> OrderOperationResponse:
        """
        Cancel an order.

        Args:
            account_seq: Account sequence number
            order_id: Order ID to cancel

        Returns:
            OrderOperationResponse
        """
        response_data = self._make_request(
            method="POST",
            endpoint=f"/api/v1/orders/{order_id}/cancel",
            json={},
            account_seq=account_seq,
        )
        return OrderOperationResponse.from_dict(response_data.get("result", {}))


class OrderHistoryMixin:
    """Mixin providing Order History API methods."""

    def get_orders(
        self,
        account_seq: int,
        status: str = "OPEN",
        symbol: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedOrderResponse:
        """
        Get order list.

        Args:
            account_seq: Account sequence number
            status: OPEN (in-progress orders). CLOSED is not yet supported by the API.
            symbol: Filter by symbol (optional)
            from_date: Start date filter YYYY-MM-DD (only applies to OPEN status)
            to_date: End date filter YYYY-MM-DD (only applies to OPEN status)
            cursor: Pagination cursor. Pass previous response's `nextCursor` for next page.
            limit: Max number of orders per page

        Returns:
            PaginatedOrderResponse
        """
        params = {"status": status}
        if symbol:
            params["symbol"] = symbol
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if cursor:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/orders",
            params=params,
            account_seq=account_seq,
        )
        return PaginatedOrderResponse.from_dict(response_data.get("result", {}))

    def get_order(self, account_seq: int, order_id: str) -> Order:
        """
        Get order details.

        Args:
            account_seq: Account sequence number
            order_id: Order ID

        Returns:
            Order
        """
        response_data = self._make_request(
            method="GET",
            endpoint=f"/api/v1/orders/{order_id}",
            account_seq=account_seq,
        )
        return Order.from_dict(response_data.get("result", {}))


class OrderInfoMixin:
    """Mixin providing Order Info API methods."""

    def get_buying_power(self, account_seq: int, currency: str) -> BuyingPowerResponse:
        """
        Get buying power.

        Args:
            account_seq: Account sequence number
            currency: Currency code (KRW or USD)

        Returns:
            BuyingPowerResponse
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/buying-power",
            params={"currency": currency},
            account_seq=account_seq,
        )
        return BuyingPowerResponse.from_dict(response_data.get("result", {}))

    def get_sellable_quantity(self, account_seq: int, symbol: str) -> SellableQuantityResponse:
        """
        Get sellable quantity for a symbol.

        Args:
            account_seq: Account sequence number
            symbol: Stock symbol

        Returns:
            SellableQuantityResponse
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/sellable-quantity",
            params={"symbol": symbol},
            account_seq=account_seq,
        )
        return SellableQuantityResponse.from_dict(response_data.get("result", {}))

    def get_commissions(self, account_seq: int) -> List[Commission]:
        """
        Get commission rates for all markets.

        Args:
            account_seq: Account sequence number

        Returns:
            List of Commission
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/commissions",
            account_seq=account_seq,
        )
        return [Commission.from_dict(c) for c in response_data.get("result", [])]
