"""
Market Info API methods for TossInvestClient.
"""

from typing import Optional

from py_toss_invest.types.market_info import (
    ExchangeRateResponse,
    KrMarketCalendarResponse,
    UsMarketCalendarResponse,
)


class MarketInfoMixin:
    """Mixin providing Market Info API methods."""

    def get_exchange_rate(
        self,
        base_currency: str,
        quote_currency: str,
        date_time: Optional[str] = None,
    ) -> ExchangeRateResponse:
        """
        Get KRW/USD exchange rate.

        Args:
            base_currency: Base currency (KRW or USD)
            quote_currency: Quote currency (KRW or USD)
            date_time: Optional specific datetime (ISO 8601). Returns current rate if omitted.

        Returns:
            ExchangeRateResponse
        """
        params = {
            "baseCurrency": base_currency,
            "quoteCurrency": quote_currency,
        }
        if date_time is not None:
            params["dateTime"] = date_time

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/exchange-rate",
            params=params,
        )
        return ExchangeRateResponse.from_dict(response_data.get("result", {}))

    def get_kr_market_calendar(
        self, date: Optional[str] = None
    ) -> KrMarketCalendarResponse:
        """
        Get KR (domestic) market trading hours for prev/today/next business days.

        Args:
            date: Reference date (YYYY-MM-DD). Uses today if omitted.

        Returns:
            KrMarketCalendarResponse
        """
        params = {}
        if date is not None:
            params["date"] = date

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/market-calendar/KR",
            params=params,
        )
        return KrMarketCalendarResponse.from_dict(response_data.get("result", {}))

    def get_us_market_calendar(
        self, date: Optional[str] = None
    ) -> UsMarketCalendarResponse:
        """
        Get US market trading hours for prev/today/next business days.

        Args:
            date: Reference date (YYYY-MM-DD, US local date). Uses today if omitted.

        Returns:
            UsMarketCalendarResponse
        """
        params = {}
        if date is not None:
            params["date"] = date

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/market-calendar/US",
            params=params,
        )
        return UsMarketCalendarResponse.from_dict(response_data.get("result", {}))
