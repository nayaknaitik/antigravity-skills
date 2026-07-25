---
name: high-frequency-backend
description: Focuses on language engineering standards across Rust, Java, and Go for high frequency systems.
---
# High Frequency Backend

## Mandatory Requirements
1. **ABSOLUTE BAN ON FLOATING POINT MATH**: Ban `f32`/`f64`, `float`, and `double` for currency/prices. Enforce `rust_decimal`, `BigDecimal`, or fixed-point integer ticks.
2. **GC & Latency Profiles**: Java Virtual Threads GC tuning rules (zero-allocation hot paths, Epsilon/ZGC rules); Go goroutine leak prevention & channel rate-limiting.
3. **Determinism**: Event-sourcing and immutable state machines to guarantee deterministic replay safety during post-incident recovery.
