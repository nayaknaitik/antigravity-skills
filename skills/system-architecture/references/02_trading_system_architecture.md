# Quantitative Trading Platform System Architecture Reference

## 1. Overview
This reference guide details specialized domain patterns, architectural blueprints, performance constraints, and state management rules for high-performance quantitative trading platforms.

---

## 2. Core Trading Platform Subsystems

```mermaid
flowchart TD
    MD[Market Data Feeds (L1/L2/L3)] --> FeedHandler[Feed Handler & Normalizer]
    FeedHandler --> TickBus[Shared Memory / Market Data Bus]
    TickBus --> Risk[Pre-Trade Risk Engine]
    TickBus --> Strat[Strategy Engine / AI Prediction]
    Strat --> Signal[Signal / Order Intent]
    Signal --> Risk
    Risk -- Approved -- OMS[Order Management System (OMS)]
    OMS --> EMS[Execution Management System (EMS)]
    EMS --> FIX[FIX Protocol / Exchange Gateway]
    FIX --> Exchange[Exchange / Market Venue]
    Exchange -- Execution Report -- FIX
    FIX --> EMS
    EMS --> OMS
    OMS --> Audit[Audit & Compliance Log]
    OMS --> Portfolio[Portfolio & Position Management]
    OMS --> PostRisk[Post-Trade Risk & Margin Engine]
```

---

## 3. Subsystem Breakdown & Architecture Rules

### 3.1 Market Data System (MDS)
- **Ingestion**: Multi-venue feed handlers supporting L1 (Top of Book), L2 (Market Depth), and L3 (Full Order Book / Tick-by-Tick).
- **Normalizer**: Convert exchange-native binary protocols (SBE, ITCH, FIX/FAST) into internal zero-copy data structures (`Tick`, `DepthUpdate`, `Trade`).
- **Storage Strategy**:
  - **Hot Path**: Ring buffer (Disruptor pattern) / Shared Memory for sub-microsecond local inter-process communication.
  - **Warm Path**: ClickHouse / QuestDB for real-time tick querying and intraday analytics.
  - **Cold Path**: Parquet files on S3/Ceph organized by date/symbol for quantitative backtesting.

### 3.2 Pre-Trade Risk Engine
- **Constraint**: Ultra-low latency ($p99 < 100\mu\text{s}$). Must execute synchronously *before* order routing.
- **Risk Checks**:
  1. Maximum Order Quantity / Value Limit.
  2. Maximum Position Limit per Symbol/Asset Class.
  3. Daily Loss Limit / Fat Finger Limit.
  4. Account Margin Availability.
  5. Short Sale Borrow Availability.
  6. Rate Limiting / Order-to-Trade Ratio (OTR).
- **Architecture**: In-memory state cache with lock-free atomic updates. Zero database queries on critical risk path.

### 3.3 Order Management System (OMS)
- **Responsibility**: State tracking, order lifecycle management, client/parent order management, execution allocation.
- **State Machine**:
  - `PendingNew` $\rightarrow$ `New` $\rightarrow$ `PartiallyFilled` $\rightarrow$ `Filled` / `Canceled` / `Rejected` / `Expired`.
- **Durability & Recovery**: Write-ahead logging (WAL) or Transactional Outbox pattern to PostgreSQL. Fast recovery from crash by replaying log.

### 3.4 Execution Management System (EMS) & Gateways
- **Responsibility**: Smart Order Routing (SOR), execution algorithms (TWAP, VWAP, Implementation Shortfall), FIX session protocol management.
- **Concurrency Model**: Dedicated single-threaded event loop per FIX session to prevent lock contention.

### 3.5 Strategy & AI Prediction Engine
- **Responsibility**: Real-time signal calculation, quantitative model inference, automated order generation.
- **Deterministic Backtesting vs Live Trading Isolation**:
  - Shared execution code via Interface abstractions.
  - Event loop backtesting clock for zero lookahead bias.

### 3.6 Portfolio & Position Management Service
- **Responsibility**: Real-time Mark-to-Market (MtM) calculation, realized/unrealized PnL, leverage monitoring, historical portfolio snapshots.
- **Consistency**: Strong consistency for settled balances, eventual consistency for streaming visual PnL dashboards.

---

## 4. Latency Budgeting & High-Performance Engineering

| Component | Target Latency Budget ($p99$) | Memory / Threading Model |
| :--- | :--- | :--- |
| **Market Data Normalization** | $< 50\mu\text{s}$ | Zero-copy byte buffers, direct memory allocation |
| **Pre-Trade Risk Checks** | $< 100\mu\text{s}$ | In-memory atomic state, single-writer pattern |
| **OMS State Update** | $< 500\mu\text{s}$ | Asynchronous WAL / Ringbuffer logging |
| **FIX Gateway Processing** | $< 250\mu\text{s}$ | Non-blocking NIO / epoll socket loops |
| **AI Inference Engine** | $< 5\text{ms}$ | C++ ONNX Runtime / TensorRT GPU batching |
