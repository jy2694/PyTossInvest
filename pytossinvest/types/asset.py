"""
Asset API response dataclasses.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Price:
    """Multi-currency amount. Each field represents only that currency's holdings."""

    krw: str
    usd: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Price":
        return cls(krw=data.get("krw", "0"), usd=data.get("usd"))


@dataclass
class Cost:
    """Cost breakdown for a holding."""

    commission: str
    tax: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Cost":
        return cls(commission=data.get("commission"), tax=data.get("tax"))


@dataclass
class MarketValue:
    """Market valuation for a single holding (in holding's currency)."""

    purchaseAmount: str
    amount: str
    amountAfterCost: str

    @classmethod
    def from_dict(cls, data: dict) -> "MarketValue":
        return cls(
            purchaseAmount=data.get("purchaseAmount"),
            amount=data.get("amount"),
            amountAfterCost=data.get("amountAfterCost"),
        )


@dataclass
class ProfitLoss:
    """Profit/loss for a single holding (in holding's currency)."""

    amount: str
    amountAfterCost: str
    rate: str
    rateAfterCost: str

    @classmethod
    def from_dict(cls, data: dict) -> "ProfitLoss":
        return cls(
            amount=data.get("amount"),
            amountAfterCost=data.get("amountAfterCost"),
            rate=data.get("rate"),
            rateAfterCost=data.get("rateAfterCost"),
        )


@dataclass
class DailyProfitLoss:
    """Daily profit/loss for a single holding (in holding's currency)."""

    amount: str
    rate: str

    @classmethod
    def from_dict(cls, data: dict) -> "DailyProfitLoss":
        return cls(amount=data.get("amount"), rate=data.get("rate"))


@dataclass
class HoldingsItem:
    """Single stock holding."""

    symbol: str
    name: str
    marketCountry: str
    currency: str
    quantity: str
    lastPrice: str
    averagePurchasePrice: str
    marketValue: MarketValue
    profitLoss: ProfitLoss
    dailyProfitLoss: DailyProfitLoss
    cost: Cost

    @classmethod
    def from_dict(cls, data: dict) -> "HoldingsItem":
        return cls(
            symbol=data.get("symbol"),
            name=data.get("name"),
            marketCountry=data.get("marketCountry"),
            currency=data.get("currency"),
            quantity=data.get("quantity"),
            lastPrice=data.get("lastPrice"),
            averagePurchasePrice=data.get("averagePurchasePrice"),
            marketValue=MarketValue.from_dict(data.get("marketValue", {})),
            profitLoss=ProfitLoss.from_dict(data.get("profitLoss", {})),
            dailyProfitLoss=DailyProfitLoss.from_dict(data.get("dailyProfitLoss", {})),
            cost=Cost.from_dict(data.get("cost", {})),
        )


@dataclass
class OverviewMarketValue:
    """Total market value across all holdings."""

    amount: Price
    amountAfterCost: Price

    @classmethod
    def from_dict(cls, data: dict) -> "OverviewMarketValue":
        return cls(
            amount=Price.from_dict(data.get("amount", {})),
            amountAfterCost=Price.from_dict(data.get("amountAfterCost", {})),
        )


@dataclass
class OverviewProfitLoss:
    """Total profit/loss across all holdings."""

    amount: Price
    amountAfterCost: Price
    rate: str
    rateAfterCost: str

    @classmethod
    def from_dict(cls, data: dict) -> "OverviewProfitLoss":
        return cls(
            amount=Price.from_dict(data.get("amount", {})),
            amountAfterCost=Price.from_dict(data.get("amountAfterCost", {})),
            rate=data.get("rate"),
            rateAfterCost=data.get("rateAfterCost"),
        )


@dataclass
class OverviewDailyProfitLoss:
    """Total daily profit/loss across all holdings."""

    amount: Price
    rate: str

    @classmethod
    def from_dict(cls, data: dict) -> "OverviewDailyProfitLoss":
        return cls(
            amount=Price.from_dict(data.get("amount", {})),
            rate=data.get("rate"),
        )


@dataclass
class HoldingsOverview:
    """Portfolio holdings overview."""

    totalPurchaseAmount: Price
    marketValue: OverviewMarketValue
    profitLoss: OverviewProfitLoss
    dailyProfitLoss: OverviewDailyProfitLoss
    items: List[HoldingsItem]

    @classmethod
    def from_dict(cls, data: dict) -> "HoldingsOverview":
        return cls(
            totalPurchaseAmount=Price.from_dict(data.get("totalPurchaseAmount", {})),
            marketValue=OverviewMarketValue.from_dict(data.get("marketValue", {})),
            profitLoss=OverviewProfitLoss.from_dict(data.get("profitLoss", {})),
            dailyProfitLoss=OverviewDailyProfitLoss.from_dict(data.get("dailyProfitLoss", {})),
            items=[HoldingsItem.from_dict(item) for item in data.get("items", [])],
        )
