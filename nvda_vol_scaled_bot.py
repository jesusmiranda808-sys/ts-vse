import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from ta.trend import EMAIndicator, SMAIndicator
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator


# ============================
# CONFIG
# ============================
SYMBOL = "NVDA"

EMA_LEN = 20
SMA_LEN = 50
ATR_LEN = 14
RSI_LEN = 14

TARGET_ATR_PCT = 0.02     # volatility target
MAX_EXPOSURE = 1.0
MIN_EXPOSURE = 0.0

START = "2021-01-01T00:00:00Z"
END   = "2026-01-01T00:00:00Z"


# ============================
# DATA
# ============================
def get_price_data(symbol, start, end):
    api_key = os.getenv("ALPACA_API_KEY")
    api_secret = os.getenv("ALPACA_API_SECRET")

    if not api_key or not api_secret:
        raise RuntimeError("Missing Alpaca API credentials.")

    client = StockHistoricalDataClient(api_key, api_secret)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        adjustment="all"
    )

    df = client.get_stock_bars(request).df

    # Handle Alpaca multi-index (symbol, timestamp)
    if isinstance(df.index, pd.MultiIndex):
        df = df.xs(symbol, level=0)

    df.sort_index(inplace=True)
    return df


# ============================
# INDICATORS
# ============================
def add_indicators(df):
    df["ema_fast"] = EMAIndicator(df["close"], EMA_LEN).ema_indicator()
    df["sma_slow"] = SMAIndicator(df["close"], SMA_LEN).sma_indicator()

    df["atr"] = AverageTrueRange(
        df["high"], df["low"], df["close"], ATR_LEN
    ).average_true_range()

    df["atr_pct"] = df["atr"] / df["close"]

    df["rsi"] = RSIIndicator(df["close"], RSI_LEN).rsi()

    return df


# ============================
# STRATEGY
# ============================
def build_strategy(df):
    # Trend signal
    df["signal"] = np.where(df["ema_fast"] > df["sma_slow"], 1.0, 0.0)

    # Volatility-scaled exposure
    df["raw_weight"] = TARGET_ATR_PCT / df["atr_pct"]
    df["weight"] = df["raw_weight"].clip(MIN_EXPOSURE, MAX_EXPOSURE)

    df["position"] = df["signal"] * df["weight"]
    return df


# ============================
# BACKTEST
# ============================
def run_backtest(df):
    df["market_return"] = df["close"].pct_change()
    df["strategy_return"] = df["position"].shift(1) * df["market_return"]

    df["equity_strategy"] = (1 + df["strategy_return"].fillna(0)).cumprod()
    df["equity_buy_hold"] = (1 + df["market_return"].fillna(0)).cumprod()

    return df


def compute_drawdown(equity):
    peak = equity.cummax()
    return (equity - peak) / peak


# ============================
# MAIN
# ============================
def main():
    df = get_price_data(SYMBOL, START, END)
    df = add_indicators(df)
    df.dropna(inplace=True)

    df = build_strategy(df)
    df = run_backtest(df)

    df["dd_strategy"] = compute_drawdown(df["equity_strategy"])
    df["dd_buy_hold"] = compute_drawdown(df["equity_buy_hold"])

    print("\nFinal Results")
    print("----------------------------")
    print(f"Strategy multiple:  {df['equity_strategy'].iloc[-1]:.2f}x")
    print(f"Buy & Hold multiple:{df['equity_buy_hold'].iloc[-1]:.2f}x")

    # ============================
    # FIGURE 1 — EQUITY CURVES
    # ============================
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["equity_strategy"], label="Strategy")
    plt.plot(df.index, df["equity_buy_hold"], label="Buy & Hold", alpha=0.7)
    plt.title("NVDA — Equity Curves")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ============================
    # FIGURE 2 — DRAWDOWNS
    # ============================
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["dd_strategy"], label="Strategy Drawdown")
    plt.plot(df.index, df["dd_buy_hold"], label="Buy & Hold Drawdown", alpha=0.7)
    plt.title("NVDA — Drawdowns")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ============================
    # FIGURE 3 — VOLATILITY & EXPOSURE
    # ============================
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["atr_pct"], label="ATR %", alpha=0.7)
    plt.plot(df.index, df["position"], label="Position Size", alpha=0.9)
    plt.title("NVDA — Volatility & Exposure")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
