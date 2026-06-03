# py-toss-invest

토스증권 Open API 비공식 Python 클라이언트 라이브러리입니다.

> [!IMPORTANT]
> 본 클라이언트 라이브러리는 토스증권 Open API가 사전예약 상태임에 따라 실호출 테스트가 되지 않은 상태입니다.

## 설치

```bash
pip install py-toss-invest
```

## 빠른 시작

```python
from py_toss_invest import TossInvestClient

client = TossInvestClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
client.authenticate()
```

Context manager 사용:

```python
with TossInvestClient(client_id="...", client_secret="...") as client:
    client.authenticate()
    accounts = client.get_accounts()
```

---

## API 레퍼런스

### 인증

```python
token = client.authenticate()
# token.access_token, token.token_type, token.expires_in

# 토큰 만료 시 재발급
client.refresh_token()
```

### Market Data

| 메서드 | 설명 |
|--------|------|
| `get_orderbook(symbol)` | 호가 조회 |
| `get_prices(symbols)` | 현재가 조회 (최대 200개) |
| `get_trades(symbol, count)` | 최근 체결 내역 조회 |
| `get_price_limits(symbol)` | 상/하한가 조회 |
| `get_candles(symbol, interval, count, before, adjusted)` | 캔들 차트 조회 |

```python
# 호가
orderbook = client.get_orderbook("005930")
for ask in orderbook.asks:
    print(f"매도 {ask.price} x {ask.volume}")

# 현재가 (다건)
prices = client.get_prices(["005930", "AAPL"])
for p in prices:
    print(f"{p.symbol}: {p.lastPrice} {p.currency}")

# 최근 체결 (최대 50건)
trades = client.get_trades("005930", count=10)
for t in trades:
    print(f"{t.timestamp}: {t.price} x {t.volume}")

# 상/하한가
limits = client.get_price_limits("005930")
print(f"상한 {limits.upperLimitPrice}, 하한 {limits.lowerLimitPrice}")

# 캔들 (1d 일봉, 1m 분봉)
candles = client.get_candles("005930", interval="1d", count=20)
for c in candles.candles:
    print(f"{c.timestamp}: O={c.openPrice} H={c.highPrice} L={c.lowPrice} C={c.closePrice}")

# 다음 페이지
if candles.nextBefore:
    next_page = client.get_candles("005930", interval="1d", before=candles.nextBefore)
```

### Market Info

| 메서드 | 설명 |
|--------|------|
| `get_exchange_rate(base_currency, quote_currency, date_time)` | 환율 조회 |
| `get_kr_market_calendar(date)` | 국내 장 운영 시간 조회 |
| `get_us_market_calendar(date)` | 미국 장 운영 시간 조회 |

```python
# 환율 (1분 주기 갱신, 참고용)
rate = client.get_exchange_rate("USD", "KRW")
print(f"USD/KRW: {rate.rate} (유효: {rate.validFrom} ~ {rate.validUntil})")

# 국내 장 운영 시간
kr_cal = client.get_kr_market_calendar()
today = kr_cal.today
if today.integrated and today.integrated.regularMarket:
    reg = today.integrated.regularMarket
    print(f"정규장: {reg.startTime} ~ {reg.endTime}")

# 미국 장 운영 시간
us_cal = client.get_us_market_calendar()
today = us_cal.today
if today.regularMarket:
    print(f"정규장: {today.regularMarket.startTime} ~ {today.regularMarket.endTime}")
```

### Stock Info

| 메서드 | 설명 |
|--------|------|
| `get_stocks(symbols)` | 종목 기본 정보 조회 (최대 200개) |
| `get_stock_warnings(symbol)` | 매수 유의사항 조회 |

```python
# 종목 기본 정보
stocks = client.get_stocks(["005930", "AAPL"])
for s in stocks:
    print(f"{s.symbol} {s.name} ({s.market}) - {s.status}")
    if s.koreanMarketDetail:
        print(f"  KRX 거래정지: {s.koreanMarketDetail.krxTradingSuspended}")

# 매수 유의사항 (활성 경고만 반환, 없으면 빈 배열)
warnings = client.get_stock_warnings("005930")
for w in warnings:
    print(f"{w.warningType} ({w.exchange}): {w.startDate} ~ {w.endDate}")
```

### Account

| 메서드 | 설명 |
|--------|------|
| `get_accounts()` | 계좌 목록 조회 |

```python
accounts = client.get_accounts()
for acc in accounts:
    print(f"계좌번호: {acc.accountNo}, seq: {acc.accountSeq}, 유형: {acc.accountType}")

account_seq = accounts[0].accountSeq
```

### Asset

| 메서드 | 설명 |
|--------|------|
| `get_holdings(account_seq, symbol)` | 보유 주식 조회 |

```python
# 전체 보유 종목
holdings = client.get_holdings(account_seq)
print(f"KRW 투자원금: {holdings.totalPurchaseAmount.krw}")
print(f"손익률: {holdings.profitLoss.rate}")

for item in holdings.items:
    print(f"{item.symbol} {item.name}: {item.quantity}주, 현재가 {item.lastPrice} {item.currency}")
    print(f"  손익: {item.profitLoss.amount} ({item.profitLoss.rate})")

# 특정 종목만 필터링
holdings = client.get_holdings(account_seq, symbol="005930")
```

### Order

| 메서드 | 설명 |
|--------|------|
| `create_order(...)` | 주문 생성 |
| `modify_order(account_seq, order_id, order_type, price, quantity)` | 주문 정정 |
| `cancel_order(account_seq, order_id)` | 주문 취소 |

```python
# 국내 지정가 매수
result = client.create_order(
    account_seq=account_seq,
    symbol="005930",
    side="BUY",
    order_type="LIMIT",
    quantity="10",
    price="70000",
)
order_id = result.orderId

# 미국 시장가 매수 (금액 기준, 정규장만 가능)
result = client.create_order(
    account_seq=account_seq,
    symbol="AAPL",
    side="BUY",
    order_type="MARKET",
    order_amount="100.00",
)

# 미국 LOC 주문 (LIMIT + CLS)
result = client.create_order(
    account_seq=account_seq,
    symbol="AAPL",
    side="BUY",
    order_type="LIMIT",
    time_in_force="CLS",
    quantity="5",
    price="185.50",
)

# 주문 정정 (국내: 가격+수량, 미국: 가격만)
client.modify_order(account_seq, order_id, order_type="LIMIT", price="71000", quantity="15")

# 주문 취소
client.cancel_order(account_seq, order_id)
```

### Order History

| 메서드 | 설명 |
|--------|------|
| `get_orders(account_seq, status, symbol, from_date, to_date)` | 주문 목록 조회 |
| `get_order(account_seq, order_id)` | 주문 상세 조회 |

```python
# 진행 중 주문 목록
orders = client.get_orders(account_seq, status="OPEN")
for order in orders.orders:
    print(f"{order.orderId}: {order.symbol} {order.side} {order.status}")
    print(f"  체결수량: {order.execution.filledQuantity}")

# 특정 종목 필터링
orders = client.get_orders(account_seq, status="OPEN", symbol="005930")

# 주문 상세
order = client.get_order(account_seq, order_id)
print(f"주문상태: {order.status}, 체결가: {order.execution.averageFilledPrice}")
```

### Order Info

| 메서드 | 설명 |
|--------|------|
| `get_buying_power(account_seq, currency)` | 매수 가능 금액 조회 |
| `get_sellable_quantity(account_seq, symbol)` | 판매 가능 수량 조회 |
| `get_commissions(account_seq)` | 매매 수수료 조회 |

```python
# 매수 가능 금액
bp = client.get_buying_power(account_seq, currency="KRW")
print(f"매수 가능: {bp.cashBuyingPower} {bp.currency}")

bp_usd = client.get_buying_power(account_seq, currency="USD")
print(f"매수 가능: {bp_usd.cashBuyingPower} {bp_usd.currency}")

# 판매 가능 수량
sq = client.get_sellable_quantity(account_seq, symbol="005930")
print(f"판매 가능: {sq.sellableQuantity}주")

# 수수료율
commissions = client.get_commissions(account_seq)
for c in commissions:
    print(f"{c.marketCountry}: {c.commissionRate} ({c.startDate} ~ {c.endDate})")
```

---

## 에러 처리

```python
from py_toss_invest import (
    TossInvestClient,
    APIError,
    AuthenticationError,
    InvalidCredentialsError,
    NetworkError,
    RateLimitExceededError,
    TokenExpiredError,
)

try:
    client.authenticate()
except InvalidCredentialsError:
    print("잘못된 client_id / client_secret")

try:
    accounts = client.get_accounts()
except TokenExpiredError:
    client.refresh_token()
    accounts = client.get_accounts()
except RateLimitExceededError as e:
    print(f"Rate limit 초과: {e}")
except APIError as e:
    print(f"API 오류 [{e.code}]: {e.message}")
except NetworkError as e:
    print(f"네트워크 오류: {e}")
```

---

## 지원 환경

- Python 3.8+
- `requests` >= 2.25.0

## 라이선스

MIT License
