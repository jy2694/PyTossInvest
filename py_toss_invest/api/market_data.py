"""
Market Data API methods for TossInvestClient.
"""

from typing import List, Optional

from py_toss_invest.types import (
    CandlePageResponse,
    OrderbookResponse,
    PriceLimitResponse,
    PriceResponse,
    Trade,
)


class MarketDataMixin:
    """Mixin providing Market Data API methods."""

    def get_orderbook(self, symbol: str) -> OrderbookResponse:
        """
        Get order book (호가) for a symbol.

        Args:
            symbol: Stock symbol (e.g., "005930" for KR, "AAPL" for US)

        Returns:
            OrderbookResponse
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/orderbook",
            params={"symbol": symbol},
        )
        return OrderbookResponse.from_dict(response_data.get("result"))

    def get_prices(self, symbols: List[str]) -> List[PriceResponse]:
        """
        Get current prices (현재가) for one or more symbols (max 200).

        Args:
            symbols: List of stock symbols, e.g. ["005930", "AAPL"]

        Returns:
            List of PriceResponse
        """
        if len(symbols) > 200:
            raise ValueError("Maximum 200 symbols allowed")

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/prices",
            params={"symbols": ",".join(symbols)},
        )
        return [PriceResponse.from_dict(item) for item in response_data.get("result", [])]

    def get_trades(self, symbol: str, count: Optional[int] = None) -> List[Trade]:
        """
        Get recent trades (최근 체결) for a symbol.

        Args:
            symbol: Stock symbol
            count: Number of trades to return (max 50, default 50)

        Returns:
            List of Trade
        """
        params = {"symbol": symbol}
        if count is not None:
            params["count"] = count

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/trades",
            params=params,
        )
        return [Trade.from_dict(item) for item in response_data.get("result", [])]

    def get_price_limits(self, symbol: str) -> PriceLimitResponse:
        """
        Get price limits (상/하한가) for a symbol.

        Args:
            symbol: Stock symbol

        Returns:
            PriceLimitResponse
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/price-limits",
            params={"symbol": symbol},
        )
        return PriceLimitResponse.from_dict(response_data.get("result"))

    def get_candles(
        self,
        symbol: str,
        interval: str = "1d",
        count: Optional[int] = None,
        before: Optional[str] = None,
        adjusted: Optional[bool] = None,
    ) -> CandlePageResponse:
        """
        Get candle chart (캔들 차트) data.

        Args:
            symbol: Stock symbol
            interval: Candle interval - "1m" (1-minute) or "1d" (1-day, default)
            count: Number of candles (max 200, default 100)
            before: Pagination cursor (exclusive, ISO 8601). Returns candles before this time.
                    Pass previous response's `nextBefore` for next page.
            adjusted: Whether to apply adjusted prices (default True)

        Returns:
            CandlePageResponse
        """
        if count is not None and count > 200:
            raise ValueError("Maximum 200 candles allowed")

        params = {"symbol": symbol, "interval": interval}
        if count is not None:
            params["count"] = count
        if before is not None:
            params["before"] = before
        if adjusted is not None:
            params["adjusted"] = adjusted

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/candles",
            params=params,
        )
        return CandlePageResponse.from_dict(response_data.get("result"))
