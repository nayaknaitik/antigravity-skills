# 05. Performance, Scalability & Testing Review Standards

This reference specifies audit standards for latency budgeting, allocation profiling, horizontal scalability, and test quality.

---

## 1. Performance & Latency Audit

1. **P95 / P99 Latency Budgeting**: Endpoints MUST meet latency SLOs (P95 < 100ms, P99 < 250ms).
2. **Allocation Reduction in Hot Paths**: Avoid unnecessary object instantiations or string concatenations inside loops.
3. **Caching & Cache Stampede**: Mandatory TTL on Redis cache keys; use SingleFlight / distributed locks for hot key calculation.

---

## 2. Scalability & Load Distribution Audit

1. **Stateless Service Process**: Nodes MUST NOT hold in-memory user sessions between requests.
2. **Resource Requests & Limits**: Kubernetes manifests MUST declare explicit CPU and Memory requests and limits.

---

## 3. Testing Quality Audit

1. **Test Coverage Threshold**: Unit tests MUST cover at least **70%** of application code.
2. **Integration Verification**: DB queries and event listeners MUST be tested against real containerized backing infrastructure (Testcontainers).
3. **No Flaky Tests**: Tests containing non-deterministic sleeps or external network dependencies are prohibited.
