Volatility-Scaled Trend Research Template

A lightweight Python research scaffold for studying how simple trend signals behave when combined with volatility-scaled exposure across assets and market regimes.
This project is educational and exploratory by design. The goal is not return maximization or production deployment, but understanding risk behavior, drawdowns, and regime dependence in trend-following systems.

Motivation

Trend-following strategies are often evaluated primarily on headline returns, despite being highly sensitive to volatility regimes and exposure management. In practice, volatility targeting can materially alter both performance and drawdown characteristics.

This template separates:

Directional intent (trend signal)
Risk management (volatility-scaled exposure)
so that the impact of exposure control can be studied independently of signal design.

Method Overview

Trend Signal
Long exposure when EMA (fast) > SMA (slow)
Flat otherwise
Volatility Measure
Average True Range (ATR), normalized as ATR%

Exposure Scaling

Position size scales inversely with realized volatility
Higher volatility → reduced exposure
Lower volatility → increased exposure (capped)

Benchmark

Buy & hold of the same asset

Outputs

The template produces three core diagnostics:
Equity Curves
Strategy vs buy & hold performance
Drawdowns
Comparative downside behavior and recovery dynamics
Volatility & Exposure
Relationship between realized volatility and position sizing
These views are intended to support interpretation, not performance marketing.

Project Structure
volatility-scaled-trend-template/
│
├── volatility_scaled_trend.py   # Main research script
├── README.md                    # Project overview
└── requirements.txt             # Dependencies (optional)

Getting Started

Requirements

Python 3.9+
pandas
numpy
matplotlib
ta (technical indicators)
Alpaca Market Data API access (paper trading keys)

Installation
pip install pandas numpy matplotlib ta alpaca-py

Set Alpaca API credentials as environment variables:
export ALPACA_API_KEY="YOUR_KEY"
export ALPACA_API_SECRET="YOUR_SECRET"

Running the Template
Edit configuration parameters at the top of the script:

SYMBOL = "NVDA"
START  = "2021-01-01"
END    = "2026-01-01"

EMA_LEN = 20
SMA_LEN = 50
ATR_LEN = 14
TARGET_ATR_PCT = 0.02

Run:
python volatility_scaled_trend.py

Intended Use
This project is suitable for:
Research experimentation
Educational demonstrations
Portfolio and regime analysis
Extending to other assets or markets
It is not intended to be:
A trading bot
An alpha signal
A production-ready system

Key Takeaways (Typical Findings)

Volatility targeting can significantly reduce drawdowns
Risk-managed strategies may underperform buy & hold in strong bull markets
Exposure management often dominates signal selection
Strategy evaluation is incomplete without drawdown analysis

Limitations

No transaction costs or slippage
Single-asset backtest
No portfolio construction layer
Simplified execution assumptions

Results should be interpreted as behavioral insights, not investable performance.


License & Disclaimer
This project is released for educational and research purposes only.
See the LICENSE file for details.

Acknowledgements
Inspired by practitioner literature on trend following, volatility targeting, and risk-managed portfolio construction.
