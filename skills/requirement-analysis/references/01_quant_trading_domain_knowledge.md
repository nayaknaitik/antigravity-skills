# Quantitative Trading & Financial Systems Domain Knowledge Base

## 1. Core System Modules & Boundaries

### 1.1 Quantitative Research & Alpha Discovery
- **Signal Discovery**: Feature engineering from tick data, order book dynamics, market sentiment, macro factors, and alternative data.
- **Statistical Modeling**: Time-series analysis, cointegration, mean reversion, statistical arbitrage, factor models (Fama-French, Barra), machine learning (LSTM, Transformer, XGBoost).
- **Data Pipelines**: High-throughput ingestion of tick data, L1/L2/L3 order books, trade prints, quote streams, corporate actions.

### 1.2 Strategy Development & Backtesting Engine
- **Strategy Abstraction**: Event-driven strategy framework processing `on_tick()`, `on_bar()`, `on_order_book()`, `on_order_event()`.
- **Event-Driven Backtester**: Simulation of market impact, slippage, exchange queue positioning, latency, order routing, short-borrow fees, margin constraints.
- **Performance Analytics**: Sharpe Ratio, Sortino Ratio, Calmar Ratio, Maximum Drawdown (MDD), Alpha, Beta, Value at Risk (VaR), Expected Shortfall (CVaR), Profit Factor, Win/Loss Ratio.

### 1.3 Paper Trading & Live Trading Infrastructure
- **Paper Trading (Sandbox)**: Execution simulation matching live order book L2/L3 feeds with zero capital risk.
- **Live Trading Execution**: Real-time trade dispatch to exchanges (NASDAQ, CME, Binance, Coinbase, FIX Protocol gateways).

### 1.4 Market Prediction & AI Agents
- **Predictive Inference**: Microsecond-latency inference engines for price movement direction, volatility forecasting, liquidity imbalance.
- **Autonomous AI Agents**: Reinforcement Learning (RL) agents for execution optimization (TWAP, VWAP, Implementation Shortfall), multi-agent portfolio rebalancing.

### 1.5 Portfolio Management & Risk Engine
- **Portfolio Management**: Real-time position tracking, PnL attribution (realized/unrealized), multi-asset allocation, cash management, currency exposure.
- **Real-time Risk Management**: Hard limits (Max Drawdown, Max Leverage, Max Position Size, Concentration Risk), Pre-Trade Risk Checks (Fat-finger prevention, Order Rate Limiting, Margin Verification), Post-Trade Risk Metrics.

### 1.6 Market Data Infrastructure (MDI)
- **Feeds**: FIX Fast, ITCH/OUCH, SBE (Simple Binary Encoding), WebSocket, REST.
- **Normalized Data Pipeline**: Tick-by-tick normalization, order book reconstruction (L2 depth, L3 order-by-order), time-series storage (ClickHouse, TimescaleDB, KDB+).

### 1.7 Order Management System (OMS) & Execution Management System (EMS)
- **OMS**: Order state lifecycle (`PENDING_NEW`, `NEW`, `PARTIALLY_FILLED`, `FILLED`, `CANCELLED`, `REJECTED`, `EXPIRED`), order routing rules, allocation logic.
- **EMS**: Smart Order Router (SOR), algorithmic execution strategies (VWAP, TWAP, POV, Iceberg, Dark Pool routing), FIX protocol engine, microsecond execution gateways.

---

## 2. Institutional Trading Terminology & Metrics

| Term | Definition | Requirement Impact |
| :--- | :--- | :--- |
| **L1 Data** | Top of book (Best Bid / Best Ask) | Used for simple charts and basic alerts. |
| **L2 Data** | Market Depth (Aggregated price levels) | Required for order book visualization, VWAP slippage estimation. |
| **L3 Data** | Individual order prints and queue positions | Mandatory for high-frequency trading (HFT) and order queue modeling. |
| **Slippage** | Difference between expected trade price and executed price | Non-functional performance metric in strategy execution. |
| **FIX Protocol** | Financial Information eXchange messaging standard | Integration protocol requirement for exchange gateways. |
| **Sub-Millisecond Latency** | Execution latency under 1 millisecond | Strict non-functional requirement for OMS/EMS. |
| **Fat-Finger Guard** | Safety threshold preventing abnormally large orders | Mandatory pre-trade risk business rule. |
