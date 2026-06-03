"""
Market Info API response dataclasses.
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class ExchangeRateResponse:
    """
    Exchange rate information.

    Attributes:
        baseCurrency: Base currency (e.g., USD)
        quoteCurrency: Quote currency (e.g., KRW)
        rate: Buy rate (1 baseCurrency = ? quoteCurrency)
        midRate: Mid rate (bank interbank rate)
        basisPoint: Basis points vs midRate. (rate - midRate) / midRate * 10000
        rateChangeType: UP, EQUAL, or DOWN
        validFrom: Rate validity start time (ISO 8601)
        validUntil: Rate validity end time (ISO 8601)
    """

    baseCurrency: Literal["KRW", "USD"]
    quoteCurrency: Literal["KRW", "USD"]
    rate: str
    midRate: str
    basisPoint: str
    rateChangeType: Literal["UP", "EQUAL", "DOWN"]
    validFrom: str
    validUntil: str

    @classmethod
    def from_dict(cls, data: dict) -> "ExchangeRateResponse":
        return cls(
            baseCurrency=data.get("baseCurrency"),
            quoteCurrency=data.get("quoteCurrency"),
            rate=data.get("rate"),
            midRate=data.get("midRate"),
            basisPoint=data.get("basisPoint"),
            rateChangeType=data.get("rateChangeType"),
            validFrom=data.get("validFrom"),
            validUntil=data.get("validUntil"),
        )


@dataclass
class PreMarketSession:
    """KR pre-market session (NXT)."""

    startTime: str
    endTime: str
    singlePriceAuctionStartTime: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PreMarketSession":
        return cls(
            startTime=data.get("startTime"),
            endTime=data.get("endTime"),
            singlePriceAuctionStartTime=data.get("singlePriceAuctionStartTime"),
        )


@dataclass
class RegularMarketSession:
    """KR regular market session."""

    startTime: str
    endTime: str
    singlePriceAuctionStartTime: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "RegularMarketSession":
        return cls(
            startTime=data.get("startTime"),
            endTime=data.get("endTime"),
            singlePriceAuctionStartTime=data.get("singlePriceAuctionStartTime"),
        )


@dataclass
class AfterMarketSession:
    """KR after-market session (NXT)."""

    startTime: str
    endTime: str
    singlePriceAuctionEndTime: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "AfterMarketSession":
        return cls(
            startTime=data.get("startTime"),
            endTime=data.get("endTime"),
            singlePriceAuctionEndTime=data.get("singlePriceAuctionEndTime"),
        )


@dataclass
class IntegratedHour:
    """KR integrated trading hours (KRX+NXT)."""

    preMarket: Optional[PreMarketSession]
    regularMarket: Optional[RegularMarketSession]
    afterMarket: Optional[AfterMarketSession]

    @classmethod
    def from_dict(cls, data: dict) -> "IntegratedHour":
        pre = data.get("preMarket")
        regular = data.get("regularMarket")
        after = data.get("afterMarket")
        return cls(
            preMarket=PreMarketSession.from_dict(pre) if pre else None,
            regularMarket=RegularMarketSession.from_dict(regular) if regular else None,
            afterMarket=AfterMarketSession.from_dict(after) if after else None,
        )


@dataclass
class KrMarketDay:
    """KR market info for a single business day."""

    date: str
    integrated: Optional[IntegratedHour]

    @classmethod
    def from_dict(cls, data: dict) -> "KrMarketDay":
        integrated = data.get("integrated")
        return cls(
            date=data.get("date"),
            integrated=IntegratedHour.from_dict(integrated) if integrated else None,
        )


@dataclass
class KrMarketCalendarResponse:
    """KR market calendar response (prev/today/next business days)."""

    today: KrMarketDay
    previousBusinessDay: KrMarketDay
    nextBusinessDay: KrMarketDay

    @classmethod
    def from_dict(cls, data: dict) -> "KrMarketCalendarResponse":
        return cls(
            today=KrMarketDay.from_dict(data.get("today", {})),
            previousBusinessDay=KrMarketDay.from_dict(data.get("previousBusinessDay", {})),
            nextBusinessDay=KrMarketDay.from_dict(data.get("nextBusinessDay", {})),
        )


@dataclass
class UsMarketSession:
    """US market session (startTime/endTime)."""

    startTime: str
    endTime: str

    @classmethod
    def from_dict(cls, data: dict) -> "UsMarketSession":
        return cls(startTime=data.get("startTime"), endTime=data.get("endTime"))


@dataclass
class UsMarketDay:
    """US market info for a single business day. All sessions null on holidays."""

    date: str
    dayMarket: Optional[UsMarketSession]
    preMarket: Optional[UsMarketSession]
    regularMarket: Optional[UsMarketSession]
    afterMarket: Optional[UsMarketSession]

    @classmethod
    def from_dict(cls, data: dict) -> "UsMarketDay":
        def _session(key):
            v = data.get(key)
            return UsMarketSession.from_dict(v) if v else None

        return cls(
            date=data.get("date"),
            dayMarket=_session("dayMarket"),
            preMarket=_session("preMarket"),
            regularMarket=_session("regularMarket"),
            afterMarket=_session("afterMarket"),
        )


@dataclass
class UsMarketCalendarResponse:
    """US market calendar response (prev/today/next business days)."""

    today: UsMarketDay
    previousBusinessDay: UsMarketDay
    nextBusinessDay: UsMarketDay

    @classmethod
    def from_dict(cls, data: dict) -> "UsMarketCalendarResponse":
        return cls(
            today=UsMarketDay.from_dict(data.get("today", {})),
            previousBusinessDay=UsMarketDay.from_dict(data.get("previousBusinessDay", {})),
            nextBusinessDay=UsMarketDay.from_dict(data.get("nextBusinessDay", {})),
        )
