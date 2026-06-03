"""
Market Data API response dataclasses.
"""

from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class OrderbookEntry:
    """Single order book entry (bid or ask)."""

    price: str
    volume: str

    @classmethod
    def from_dict(cls, data: dict) -> "OrderbookEntry":
        return cls(price=data.get("price"), volume=data.get("volume"))


@dataclass
class OrderbookResponse:
    """
    Order book (호가) information.

    Attributes:
        timestamp: Order book timestamp (ISO 8601 format), nullable
        currency: Currency code (KRW or USD)
        asks: Sell orders (asks), ordered by price ascending
        bids: Buy orders (bids), ordered by price descending
    """

    timestamp: Optional[str]
    currency: Literal["KRW", "USD"]
    asks: List[OrderbookEntry]
    bids: List[OrderbookEntry]

    @classmethod
    def from_dict(cls, data: dict) -> "OrderbookResponse":
        asks = [OrderbookEntry.from_dict(a) for a in data.get("asks", [])]
        bids = [OrderbookEntry.from_dict(b) for b in data.get("bids", [])]
        return cls(
            timestamp=data.get("timestamp"),
            currency=data.get("currency"),
            asks=asks,
            bids=bids,
        )


@dataclass
class PriceResponse:
    """
    Current price (현재가) information.

    Attributes:
        symbol: Stock symbol
        timestamp: Price timestamp (ISO 8601 format), nullable
        lastPrice: Last trade price
        currency: Currency code (KRW or USD)
    """

    symbol: str
    timestamp: Optional[str]
    lastPrice: str
    currency: Literal["KRW", "USD"]

    @classmethod
    def from_dict(cls, data: dict) -> "PriceResponse":
        return cls(
            symbol=data.get("symbol"),
            timestamp=data.get("timestamp"),
            lastPrice=data.get("lastPrice"),
            currency=data.get("currency"),
        )


@dataclass
class Trade:
    """
    Single trade execution (체결).

    Attributes:
        price: Trade price
        volume: Traded volume
        timestamp: Trade timestamp (ISO 8601 format)
        currency: Currency code (KRW or USD)
    """

    price: str
    volume: str
    timestamp: str
    currency: Literal["KRW", "USD"]

    @classmethod
    def from_dict(cls, data: dict) -> "Trade":
        return cls(
            price=data.get("price"),
            volume=data.get("volume"),
            timestamp=data.get("timestamp"),
            currency=data.get("currency"),
        )


@dataclass
class PriceLimitResponse:
    """
    Price limits (상/하한가) information.

    Attributes:
        timestamp: Data timestamp (ISO 8601 format)
        upperLimitPrice: Upper limit price, null for markets with no limit
        lowerLimitPrice: Lower limit price, null for markets with no limit
        currency: Currency code (KRW or USD)
    """

    timestamp: str
    upperLimitPrice: Optional[str]
    lowerLimitPrice: Optional[str]
    currency: Literal["KRW", "USD"]

    @classmethod
    def from_dict(cls, data: dict) -> "PriceLimitResponse":
        return cls(
            timestamp=data.get("timestamp"),
            upperLimitPrice=data.get("upperLimitPrice"),
            lowerLimitPrice=data.get("lowerLimitPrice"),
            currency=data.get("currency"),
        )


@dataclass
class Candle:
    """
    Single candle (candlestick) data point.

    Attributes:
        timestamp: Candle start time (ISO 8601 format)
        openPrice: Opening price of the candle period
        highPrice: Highest price during the period
        lowPrice: Lowest price during the period
        closePrice: Closing price of the period
        volume: Trading volume during the period
        currency: Currency code (KRW or USD)
    """

    timestamp: str
    openPrice: str
    highPrice: str
    lowPrice: str
    closePrice: str
    volume: str
    currency: Literal["KRW", "USD"]

    @classmethod
    def from_dict(cls, data: dict) -> "Candle":
        return cls(
            timestamp=data.get("timestamp"),
            openPrice=data.get("openPrice"),
            highPrice=data.get("highPrice"),
            lowPrice=data.get("lowPrice"),
            closePrice=data.get("closePrice"),
            volume=data.get("volume"),
            currency=data.get("currency"),
        )


@dataclass
class CandlePageResponse:
    """
    Candle chart (캔들 차트) response.

    Attributes:
        candles: List of candle data points
        nextBefore: Cursor for next page (pass as `before` param), null if last page
    """

    candles: List[Candle]
    nextBefore: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "CandlePageResponse":
        candles = [Candle.from_dict(c) for c in data.get("candles", [])]
        return cls(
            candles=candles,
            nextBefore=data.get("nextBefore"),
        )
