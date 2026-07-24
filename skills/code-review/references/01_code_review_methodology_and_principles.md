# 01. Principal Code Review Methodology & Standards

This reference defines organization-wide code review standards synthesized from Google Engineering Practices, Meta Code Review Guidelines, Stripe, Uber, Netflix, Cloudflare, and AWS Builders Library.

---

## 1. Code Review Objective & Persona

Code review is our primary gate for software correctness, operational excellence, security, maintainability, and architectural consistency.

```
       +-------------------------------------------------------------+
       |             PRINCIPAL REVIEW ENGINE OBJECTIVES              |
       |  • Ensure code correctness & zero runtime memory leaks       |
       |  • Enforce zero breaking API mutations                      |
       |  • Verify 25 Production Engineering standards               |
       |  • Detect AI-generated code hallucinations & anti-patterns   |
       |  • Guarantee financial decimal precision & trade atomicity   |
       +-------------------------------------------------------------+
```

### The 5 Principles of Effective Review:
1. **Never Merge Defective Code**: A pull request (PR) MUST NOT be approved if it contains critical security flaws, race conditions, memory leaks, unhandled exceptions, or missing observability.
2. **Review Intent & Context**: Every PR MUST state *Why* the change is being made, *What* changed, and *How* it was empirically verified.
3. **Atomic PR Rule**: PRs SHOULD NOT exceed **400 lines of diff**. Large features MUST be broken down into incremental, feature-flagged PRs.
4. **Explicit Classification**:
   - `[BLOCKER]`: Critical issue requiring resolution prior to merge (e.g. security, race condition, data corruption).
   - `[WARNING]`: Non-critical performance or maintainability concern requiring author response.
   - `[NIT]`: Superficial suggestion or optional formatting improvement (non-blocking).
5. **Constructive Handoff**: Always explain *Why* an issue is flagged and provide a concrete production-grade code alternative.

---

## 2. 15 Review Dimensions Framework

Every pull request MUST be systematically audited across 15 distinct technical dimensions:

| # | Review Dimension | Key Focus Areas |
| :-: | :--- | :--- |
| **1** | **Correctness** | Logic errors, off-by-one, memory/connection leaks, unclosed handles, null safety, state corruption. |
| **2** | **Architecture** | Clean/Hexagonal boundaries, SOLID, DRY, KISS, YAGNI, package organization, DDD context. |
| **3** | **API Design** | REST/gRPC standards, idempotency keys, date-based versioning, backward compatibility, validation. |
| **4** | **Error Handling** | RFC 7807, wrapped errors, retry policies with jitter, circuit breakers, graceful shutdown. |
| **5** | **Concurrency** | Thread/goroutine safety, lock ordering, atomic counters, channel leaks, virtual thread pinning. |
| **6** | **Database** | N+1 queries, explicit locking, connection pool bounds, Flyway migrations, transaction isolation. |
| **7** | **Security** | OWASP Top 10, SQLi, XSS, CSRF, SSRF, JWT/OAuth2, zero hardcoded secrets, least privilege DB access. |
| **8** | **Performance** | Latency budgets (P95 < 100ms), allocation reduction in hot paths, streaming vs batching, pprof. |
| **9** | **Scalability** | Stateless processes, cache stampede protection, database/queue bottleneck elimination. |
| **10**| **Reliability** | Retries, static stability, fallbacks, health checks (Startup/Liveness/Readiness), chaos tolerance. |
| **11**| **Observability**| Structured JSON logging (`trace_id`, `span_id`), OpenTelemetry tracing, RED/USE metrics. |
| **12**| **Testing** | Unit test coverage (>=70%), Testcontainers integration tests, contract & mutation tests. |
| **13**| **Maintainability** | Readability, cyclomatic complexity, no magic values, comprehensive ADRs and documentation. |
| **14**| **AI Generated Code**| Hallucinated APIs, fake dependencies, tutorial-quality code, missing production resilience. |
| **15**| **Financial Systems**| `BigDecimal`/cents integer precision, currency mismatch checks, order/trade idempotency. |
