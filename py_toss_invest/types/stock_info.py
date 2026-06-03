"""
Stock Info API response dataclasses.
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class KrMarketDetail:
    """
    Korean market specific details.

    Attributes:
        liquidationTrading: Whether in liquidation trading (상장폐지 절차 중)
        nxtSupported: Whether NXT alternative exchange is supported
        krxTradingSuspended: Whether trading is suspended on KRX
        nxtTradingSuspended: Whether trading is suspended on NXT; null if NXT not supported
    """

    liquidationTrading: bool
    nxtSupported: bool
    krxTradingSuspended: bool
    nxtTradingSuspended: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "KrMarketDetail":
        return cls(
            liquidationTrading=data.get("liquidationTrading"),
            nxtSupported=data.get("nxtSupported"),
            krxTradingSuspended=data.get("krxTradingSuspended"),
            nxtTradingSuspended=data.get("nxtTradingSuspended"),
        )


@dataclass
class StockInfo:
    """
    Stock basic information.

    Attributes:
        symbol: Stock symbol (e.g., "005930" for KR, "AAPL" for US)
        name: Stock name in Korean
        englishName: Stock name in English
        isinCode: International Securities Identification Number (ISO 6166)
        market: Listed market (KOSPI, KOSDAQ, NYSE, NASDAQ, AMEX, KR_ETC, US_ETC)
        securityType: Security type (STOCK, ETF, etc.)
        isCommonShare: Whether it is a common share (보통주)
        status: Listing status (SCHEDULED, ACTIVE, DELISTED)
        currency: Currency code (KRW or USD)
        listDate: Listing date (YYYY-MM-DD), null if not available
        delistDate: Delisting date (YYYY-MM-DD), null if still active
        sharesOutstanding: Number of outstanding shares
        leverageFactor: Leverage factor for ETF/ETN, null otherwise
        koreanMarketDetail: Korean market details, null for non-KR stocks
    """

    symbol: str
    name: str
    englishName: str
    isinCode: str
    market: str
    securityType: str
    isCommonShare: bool
    status: Literal["SCHEDULED", "ACTIVE", "DELISTED"]
    currency: Literal["KRW", "USD"]
    sharesOutstanding: str
    listDate: Optional[str] = None
    delistDate: Optional[str] = None
    leverageFactor: Optional[str] = None
    koreanMarketDetail: Optional[KrMarketDetail] = None

    @classmethod
    def from_dict(cls, data: dict) -> "StockInfo":
        kr_detail = data.get("koreanMarketDetail")
        return cls(
            symbol=data.get("symbol"),
            name=data.get("name"),
            englishName=data.get("englishName"),
            isinCode=data.get("isinCode"),
            market=data.get("market"),
            securityType=data.get("securityType"),
            isCommonShare=data.get("isCommonShare"),
            status=data.get("status"),
            currency=data.get("currency"),
            sharesOutstanding=data.get("sharesOutstanding"),
            listDate=data.get("listDate"),
            delistDate=data.get("delistDate"),
            leverageFactor=data.get("leverageFactor"),
            koreanMarketDetail=KrMarketDetail.from_dict(kr_detail) if kr_detail else None,
        )


@dataclass
class StockWarning:
    """
    Stock purchase warning information.

    Warning types:
        LIQUIDATION_TRADING: 정리매매
        OVERHEATED: 단기과열
        INVESTMENT_WARNING: 투자경고
        INVESTMENT_RISK: 투자위험
        VI_STATIC: VI 정적 발동
        VI_DYNAMIC: VI 동적 발동
        VI_STATIC_AND_DYNAMIC: VI 정적+동적 동시 발동
        STOCK_WARRANTS: 신주인수권

    Attributes:
        warningType: Type of warning
        exchange: Exchange code (KRX, NXT, etc.)
        startDate: Warning start date (YYYY-MM-DD), null if unknown
        endDate: Warning end date (YYYY-MM-DD), null if ongoing
    """

    warningType: str
    exchange: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "StockWarning":
        return cls(
            warningType=data.get("warningType"),
            exchange=data.get("exchange"),
            startDate=data.get("startDate"),
            endDate=data.get("endDate"),
        )
