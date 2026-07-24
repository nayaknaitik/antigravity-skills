# Worked Example: Pre-Trade Risk Engine High-Level & Low-Level Design (HLD & LLD)

## 1. Overview
The Pre-Trade Risk Engine is a critical sub-millisecond line-of-defense component that intercepts every order before transmission to execution venues.

## 2. Ultra-Low Latency Architecture

```mermaid
flowchart LR
    OrderIn[Incoming Order Intent] --> FastCheck[Lock-Free Fast-Path Checks]
    FastCheck --> |1. Price Sanity| Check1[Price Check]
    FastCheck --> |2. Max Order Size| Check2[Max Qty Check]
    FastCheck --> |3. Position Limit| Check3[Position Limit Check]
    FastCheck --> |4. OTR Limit| Check4[Order-to-Trade Ratio Check]
    Check1 --> Decision{All Passed?}
    Check2 --> Decision
    Check3 --> Decision
    Check4 --> Decision
    Decision -- Yes --> Route[Approve & Pass to OMS]
    Decision -- No --> Reject[Reject Order & Log Audit Event]
```

## 3. Performance & Memory Blueprint
- Written in C++20 / Rust with zero memory allocation on critical check path.
- State storage: In-memory arrays indexed by `AccountID` and `SymbolID` for $O(1)$ constant time evaluation.
- Micro-benchmark Target: $p99.9 < 15\mu\text{s}$.
