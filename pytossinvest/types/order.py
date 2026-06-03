"""
Order API response dataclasses.
"""

from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class OrderExecution:
    """Order execution details."""

    filledQuantity: str
    averageFilledPrice: Optional[str]
    filledAmount: Optional[str]
    commission: Optional[str]
    tax: Optional[str]
    filledAt: Optional[str]
    settlementDate: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "OrderExecution":
        return cls(
            filledQuantity=data.get("filledQuantity"),
            averageFilledPrice=data.get("averageFilledPrice"),
            filledAmount=data.get("filledAmount"),
            commission=data.get("commission"),
            tax=data.get("tax"),
            filledAt=data.get("filledAt"),
            settlementDate=data.get("settlementDate"),
        )


@dataclass
class Order:
    """Order information."""

    orderId: str
    symbol: str
    side: Literal["BUY", "SELL"]
    orderType: Literal["LIMIT", "MARKET"]
    timeInForce: str
    status: str
    currency: str
    orderedAt: str
    execution: OrderExecution
    price: Optional[str] = None
    quantity: Optional[str] = None
    orderAmount: Optional[str] = None
    canceledAt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        execution = data.get("execution")
        return cls(
            orderId=data.get("orderId"),
            symbol=data.get("symbol"),
            side=data.get("side"),
            orderType=data.get("orderType"),
            timeInForce=data.get("timeInForce"),
            status=data.get("status"),
            currency=data.get("currency"),
            orderedAt=data.get("orderedAt"),
            execution=OrderExecution.from_dict(execution) if execution else None,
            price=data.get("price"),
            quantity=data.get("quantity"),
            orderAmount=data.get("orderAmount"),
            canceledAt=data.get("canceledAt"),
        )


@dataclass
class OrderResponse:
    """Response from order creation."""

    orderId: str
    clientOrderId: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "OrderResponse":
        return cls(
            orderId=data.get("orderId"),
            clientOrderId=data.get("clientOrderId"),
        )


@dataclass
class OrderOperationResponse:
    """Response from order modification/cancellation."""

    orderId: str

    @classmethod
    def from_dict(cls, data: dict) -> "OrderOperationResponse":
        return cls(orderId=data.get("orderId"))


@dataclass
class PaginatedOrderResponse:
    """Paginated order list response."""

    orders: List[Order]
    nextCursor: Optional[str] = None
    hasNext: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "PaginatedOrderResponse":
        orders = [Order.from_dict(o) for o in data.get("orders", [])]
        return cls(
            orders=orders,
            nextCursor=data.get("nextCursor"),
            hasNext=data.get("hasNext", False),
        )


@dataclass
class BuyingPowerResponse:
    """Buying power information."""

    currency: Literal["KRW", "USD"]
    cashBuyingPower: str

    @classmethod
    def from_dict(cls, data: dict) -> "BuyingPowerResponse":
        return cls(
            currency=data.get("currency"),
            cashBuyingPower=data.get("cashBuyingPower"),
        )


@dataclass
class SellableQuantityResponse:
    """Sellable quantity information."""

    sellableQuantity: str

    @classmethod
    def from_dict(cls, data: dict) -> "SellableQuantityResponse":
        return cls(sellableQuantity=data.get("sellableQuantity"))


@dataclass
class Commission:
    """Commission rate information for a market."""

    marketCountry: str
    commissionRate: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Commission":
        return cls(
            marketCountry=data.get("marketCountry"),
            commissionRate=data.get("commissionRate"),
            startDate=data.get("startDate"),
            endDate=data.get("endDate"),
        )
