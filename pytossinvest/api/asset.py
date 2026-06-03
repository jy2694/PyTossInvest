"""Asset API methods for TossInvestClient (Phase 5)."""

from typing import Optional

from pytossinvest.types import HoldingsOverview


class AssetMixin:
    """Mixin providing Asset API methods."""

    def get_holdings(
        self, account_seq: int, symbol: Optional[str] = None
    ) -> HoldingsOverview:
        """
        Get portfolio holdings.

        Args:
            account_seq: Account sequence number
            symbol: Filter to a single symbol (optional)

        Returns:
            HoldingsOverview: Holdings information including items and summary

        Raises:
            AuthenticationError: If not authenticated
            APIError: If API returns error
        """
        params = {}
        if symbol is not None:
            params["symbol"] = symbol

        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/holdings",
            params=params,
            account_seq=account_seq,
        )

        return HoldingsOverview.from_dict(response_data.get("result", {}))
