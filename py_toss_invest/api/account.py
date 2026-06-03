"""
Account API methods for TossInvestClient.

This module provides wrapper methods for Account API endpoints.
Methods can be added to TossInvestClient through inheritance or composition.
"""

from typing import List

from py_toss_invest.types import Account


class AccountMixin:
    """
    Mixin providing Account API methods.

    Assumes the class has _make_request method from TossInvestClient.
    """

    def get_accounts(self) -> List[Account]:
        """
        Get list of user accounts.

        Returns all accounts in normal status (excludes closed/suspended accounts).
        Currently only returns BROKERAGE type accounts.

        Returns:
            List of Account objects. Empty list if user has no accounts.

        Raises:
            AuthenticationError: If not authenticated
            APIError: If API returns error

        Example:
            >>> accounts = client.get_accounts()
            >>> for account in accounts:
            ...     print(f"{account.accountName}: {account.accountSeq}")
            ...     # Use accountSeq as X-Tossinvest-Account header for other API calls
        """
        response_data = self._make_request(
            method="GET",
            endpoint="/api/v1/accounts",
        )

        result = response_data.get("result", [])
        if isinstance(result, list):
            return [Account.from_dict(item) for item in result]
        else:
            # Shouldn't happen but handle single account response
            return [Account.from_dict(result)] if result else []
