"""
Stock Info API methods for TossInvestClient.

This module provides wrapper methods for Stock Info API endpoints.
Methods can be added to TossInvestClient through inheritance or composition.
"""

from typing import List

from pytossinvest.types import StockInfo, StockWarning


class StockInfoMixin:
    """
    Mixin providing Stock Info API methods.

    Assumes the class has _make_request method from TossInvestClient.
    """

    def get_stocks(self, symbols: List[str]) -> List[StockInfo]:
        """
        Get stock basic information.

        Args:
            symbols: List of stock symbols (max 200)
                    e.g., ["005930", "000660"] for KR or ["AAPL", "MSFT"] for US

        Returns:
            List of StockInfo objects containing basic stock information

        Raises:
            ValidationError: If more than 200 symbols provided
            NotFoundError: If any symbol not found
            APIError: If API returns error
        """
        if len(symbols) > 200:
            raise ValueError("Maximum 200 symbols allowed")

        symbol_str = ",".join(symbols)
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/stocks",
            params={"symbols": symbol_str},
        )

        result = response_data.get("result", [])
        if isinstance(result, list):
            return [StockInfo.from_dict(item) for item in result]
        else:
            # Single symbol case might return object instead of array
            return [StockInfo.from_dict(result)]

    def get_stock_warnings(self, symbol: str) -> List[StockWarning]:
        """
        Get stock purchase warnings and cautions.

        Returns active warnings for the given symbol. Active means:
        startDate <= today <= endDate (or endDate is null for ongoing warnings)

        Warnings are sorted by startDate in descending order (most recent first).

        Args:
            symbol: Stock symbol (e.g., "005930" or "AAPL")

        Returns:
            List of StockWarning objects. Empty list if no active warnings.

        Raises:
            NotFoundError: If symbol not found
            APIError: If API returns error

        Example:
            >>> warnings = client.get_stock_warnings("005930")
            >>> for warning in warnings:
            ...     print(f"{warning.warningType}: {warning.startDate} to {warning.endDate}")
        """
        response_data = self._make_request(
            method="GET",
            endpoint=f"/api/v1/stocks/{symbol}/warnings",
        )

        result = response_data.get("result", [])
        if isinstance(result, list):
            return [StockWarning.from_dict(item) for item in result]
        else:
            return [StockWarning.from_dict(result)]
