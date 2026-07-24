# 02. Correctness, Concurrency, Financial Safety & AI Code Audit

This reference details audit procedures for runtime correctness, concurrency hazards, financial decimal precision, and detecting AI-generated code anti-patterns.

---

## 1. Correctness & Resource Leak Audit

### 1. Resource Leak Detection:
- **Unclosed File Handles / DB Connections**: Every opened IO handle (file, DB rows, HTTP response body) MUST be explicitly closed using `defer` (Go), `try-with-resources` (Java), or RAII (Rust).
  - *Violation Example (Go)*: `resp, err := http.Get(url)` without `defer resp.Body.Close()`.
  - *Violation Example (Java)*: `ResultSet rs = stmt.executeQuery()` without closing `rs` or using `try-with-resources`.

### 2. Null Pointer & Optional Misuse:
- Flag any method returning `null` instead of an empty collection (`List.of()`, `Collections.emptyList()`).
- Flag direct calls to `optional.get()` without prior `isPresent()` checks.

---

## 3. Concurrency & Multi-Threading Audit

### 1. Goroutine / Thread Leaks:
- Flag any `go func()` or background thread launched without binding to `context.Context` cancellation or channel drain signal.
- Verify that worker pools gracefully drain active jobs upon shutdown.

### 2. Lock Ordering & Deadlock Hazards:
- Flag acquiring multiple mutexes out of order across different code paths (e.g. Thread 1 acquires `LockA` then `LockB`; Thread 2 acquires `LockB` then `LockA`).

### 3. Virtual Thread Carrier Pinning (Java 21+):
- Flag `synchronized` blocks/methods performing IO operations under Virtual Threads; require `ReentrantLock`.

---

## 4. Financial Systems & Trading Safety Audit

Financial, trading, OMS, EMS, and risk code MUST adhere to mathematical precision rules:

### 1. Floating-Point Money Disallowed:
- **STRICT BLOCKER**: Floating-point types (`float`, `double`, `float32`, `float64`) MUST NEVER be used for monetary amounts or currency values. Floating-point binary representation causes catastrophic rounding errors (e.g. `0.1 + 0.2 != 0.3`).
- *Mandatory Types*: Use `BigDecimal` (Java), `shopspring/decimal` (Go), or integer cents/micro-units.

### 2. Currency Matching:
- Addition or subtraction of monetary values MUST verify matching currency types (`Money.add(Money other)` must assert `this.currency == other.currency`).

### 3. Trade & Order Atomicity:
- Financial order executions and portfolio balance updates MUST occur within a single database transaction or idempotent Saga step.

---

## 5. AI-Generated Code & Hallucination Audit

AI coding tools frequently generate subtle bugs that pass surface linter checks. Reviewers MUST audit for:

1. **Hallucinated Methods / Non-Existent Flags**: Verify that imported library methods exist in target version manifests.
2. **Tutorial-Quality Code**: Code containing hardcoded localhost IPs, missing timeouts, silent `try/catch` swallowing exceptions, or missing OTel telemetry.
3. **Copy-Pasted Boilerplate**: Unused methods, dead code, or redundant comments restating obvious code actions.
