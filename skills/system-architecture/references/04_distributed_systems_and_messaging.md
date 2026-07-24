# Distributed Systems, Data Storage & Messaging Reference

## 1. Overview
This reference guide establishes technology selection rules, data partitioning strategies, messaging patterns, and caching topology across our quantitative trading platform services.

---

## 2. Data Storage Strategy

### 2.1 Primary Relational Database (PostgreSQL)
- **Role**: Source of truth for transactional data (Users, Accounts, Orders, Executions, Positions, Risk Configurations).
- **Architecture Guidelines**:
  - Use Connection Pooling (PgBouncer).
  - Explicit database transactions (`BEGIN` ... `COMMIT`) with strict isolation levels (Read Committed for standard, Repeatable Read / Serializable for position reconciliation).
  - Strict schema migrations using Flynn/Liquibase/Flyway. Never run manual DDL in production.
  - Read Replicas for reporting queries.

### 2.2 Time-Series & Market Data Database (ClickHouse / QuestDB)
- **Role**: High-throughput tick-by-tick storage, order book depth snapshots, historical bar data ($1\text{s}, 1\text{m}, 1\text{h}$).
- **Partitioning**: Partition by `toYYYYMM(timestamp)` and primary key `(symbol, timestamp)`.

### 2.3 Cache Layer (Redis / Dragonfly)
- **Role**: Low-latency session state, real-time position cache, market tick cache, rate-limiting tokens.
- **Topology**: Redis Sentinel / Cluster with AOF persistence.
- **Patterns**: Cache-aside for static/reference data, Write-through / WAL for high-speed risk state.

---

## 3. Asynchronous Messaging Architecture

### 3.1 Apache Kafka (Event Streaming Engine)
- **Role**: High-throughput distributed event streaming log.
- **Topic Naming Convention**: `<environment>.<domain>.<entity>.<event_type>.v<version>`
  - Example: `prod.trading.order.filled.v1`
  - Example: `prod.marketdata.bar.1min.v1`
- **Partitioning Strategy**: Partition key MUST be `symbol` or `account_id` to guarantee strict in-order message delivery within partition.
- **Retention Policies**:
  - Trading Events: 7 years retention (compliance requirement).
  - High-frequency market ticks: Compacted log or short TTL (24-48 hours).

### 3.2 In-Memory Pub/Sub (Redis PubSub / ZeroMQ)
- **Role**: Inter-process ultra-low-latency broadcast for intraday UI streaming (WebSocket push) and tick distribution.

---

## 4. Distributed Systems Reliability Patterns

### 4.1 Idempotency & Duplicate Prevention
- All event consumers MUST implement idempotency using explicit deduplication keys (e.g. `cl_ord_id` + `fill_id`).
- Store processed event IDs in Redis or PostgreSQL with unique constraints.

### 4.2 Circuit Breakers & Rate Limiters
- Wrap external exchange endpoints and LLM APIs with Resilience4j/Envoy circuit breakers.
- State transitions: `Closed` $\rightarrow$ `Open` (on 50% failure rate) $\rightarrow$ `Half-Open` (test request).

### 4.3 Transactional Outbox Pattern
```
[ Application Service ]
       │
       ├── 1. Write Entity State Change  ──► [ PostgreSQL Table: orders ]
       │                                         │
       └── 2. Write Domain Event Record  ──► [ PostgreSQL Table: outbox ]  (Same Local ACID Transaction)
                                                 │
                                                 ▼
                                        [ Debezium CDC / Outbox Poller ]
                                                 │
                                                 ▼
                                        [ Apache Kafka Bus ]
```
