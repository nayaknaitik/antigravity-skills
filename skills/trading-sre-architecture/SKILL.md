---
name: trading-sre-architecture
description: Focuses on broker limits, static IP routing, circuit breakers, kill switches, and infrastructure SLA.
---
# Trading SRE Architecture

## Mandatory Requirements
1. **Broker Rate Limits**: Explicit bucket limits (e.g., Zerodha 10 req/s REST limit, Groww WebSocket message caps, Kotak Neo execution SLA < 50ms).
2. **Infrastructure Guardrails**: Static IP egress routing rules, automatic reconnect logic with backoff for WebSockets.
3. **SRE Resiliency**: Mandatory global & per-strategy Kill Switch specifications, position sizing, and drawdown limits.
