"""
Account API response dataclasses.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Account:
    """
    User account information.

    Attributes:
        accountNo: Account number
        accountSeq: Account sequence key (used in X-Tossinvest-Account header)
        accountType: Account type (currently only BROKERAGE is returned)
    """

    accountNo: str
    accountSeq: int
    accountType: Literal[
        "BROKERAGE", "OVERSEAS_DERIVATIVES", "PENSION_SAVINGS", "RESHORING_INVESTMENT"
    ]

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(
            accountNo=data.get("accountNo"),
            accountSeq=data.get("accountSeq"),
            accountType=data.get("accountType"),
        )
