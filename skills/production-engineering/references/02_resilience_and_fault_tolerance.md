# 02. Resilience, Fault Tolerance & Static Stability

This reference details the mandatory resilience patterns drawn from the AWS Builders Library, Netflix Engineering, Uber Engineering, and Cloudflare Engineering.

---

## 1. Timeout Management

Unbounded network calls are the primary cause of cascading failures in distributed systems.

### Mandatory Rules:
1. **Explicit Timeouts Everywhere**: Every outbound network call (HTTP, gRPC, DB, Redis, AMQP) MUST have an explicit execution timeout configured. Default/infinite timeouts are strictly prohibited.
2. **Layered Timeout Hierarchies**: Outer timeouts must be larger than inner timeouts.
   - *Example*: Gateway HTTP Timeout (5000ms) > Service Call Timeout (2500ms) > Database Query Timeout (1000ms).
3. **Contextual Deadline Propagation**:
   - In languages supporting deadline context (Go `context.Context`, gRPC `deadline`, Rust `tokio::time::timeout`), deadline timestamps MUST be passed downstream.
   - If downstream remaining time is `< 10ms`, cancel execution immediately without making the outbound call.

---

## 2. Retry Policies, Exponential Backoff & Jitter

Blind retries under high load create retry storms that can bring down failing dependencies (AWS Builders Library recommendation).

### Standard Retry Formula:
```
sleep_time = min(cap, base * 2 ^ attempt) + random_jitter
```

### Mandatory Rules:
1. **Only Retry Transient Errors**:
   - *Retryable*: Network IO errors, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout, 429 Too Many Requests.
   - *Non-Retryable*: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity.
2. **Full Jitter Implementation**: Retries MUST apply full jitter (randomized sleep between `0` and calculated exponential backoff limit) to prevent thundering herd problems across distributed clients.
3. **Max Attempt Budgeting**: Set maximum retry attempts to **3** by default.
4. **Retry Budgets**: Clients should maintain a token bucket for retries. Retries must fail fast if retry ratio exceeds **10%** of overall request volume.

---

## 3. Circuit Breaker Pattern

Prevent services from repeatedly attempting actions that are guaranteed to fail (Netflix Hystrix / Resilience4j pattern).

```
   +---------+     Failures > Threshold     +----------+
   |         | ---------------------------> |          |
   | CLOSED  |                              |   OPEN   |
   | (Normal)| <--------------------------- |(Fast Fail|
   +---------+      Success in Half-Open    +----------+
        ^                                        |
        |                                        | Sleep Window
        |          +---------------+             | Expires
        +--------- |   HALF-OPEN   | <-----------+
                   | (Test Calls)  |
                   +---------------+
```

### Circuit Breaker States & Parameters:
- **CLOSED**: Requests flow normally. Monitor failure rate in a rolling window (e.g., last 100 calls or 10 seconds).
- **OPEN**: If failure rate exceeds threshold (e.g., **50%** failures or 5 consecutive errors), immediately reject all calls with `CircuitBreakerOpenException` without hitting downstream service.
- **HALF-OPEN**: After a sleep duration (e.g., **5000ms**), allow a limited trial batch (e.g., 5 probe requests).
  - If probes succeed -> transition to **CLOSED**.
  - If any probe fails -> transition back to **OPEN**.

---

## 4. Bulkheads & Traffic Isolation

Prevent a failure in one subsystem from consuming all thread pools or network connections in the service (Uber / Netflix pattern).

### Guidelines:
1. **Thread Pool / Connection Pool Isolation**: Assign dedicated connection pools to separate downstream dependencies. A spike in latency on Service A must not starve connection pools for Service B.
2. **Load Shedding**: When queue depth or CPU usage exceeds safety thresholds (e.g., CPU > 85%), shed non-critical requests immediately with HTTP 503.
3. **Rate Limiting**: Protect endpoints using Token Bucket or Sliding Window algorithms (e.g., 100 req/sec per tenant).

---

## 5. Static Stability & Fallback Strategies

AWS Builders Library defines **Static Stability** as the ability of a system to continue operating even when a dependency fails or is unavailable.

### Fallback Implementations:
- **Cached Fallback**: Serve slightly stale data from local memory or Redis if live call fails.
- **Degraded Response**: Return partial data (e.g., return user profile without personalized recommendations).
- **Default Fallback**: Return safe static defaults.

---

## 6. Graceful Shutdown & Cancellation

Services must shut down cleanly without dropping in-flight requests or corrupting state upon receiving termination signals (`SIGTERM`, `SIGINT`).

### 4-Phase Graceful Shutdown Protocol:
1. **Phase 1: Signal Trap & Health Update**
   - Catch `SIGTERM` / `SIGINT`. Immediately switch readiness probe to `UNHEALTHY` (HTTP 503) so Kubernetes stop sending new traffic.
2. **Phase 2: Drain In-Flight Requests**
   - Wait for load balancer to drain traffic (e.g., 5–10 seconds). Continue processing currently active requests.
3. **Phase 3: Stop Background Workers & Queue Consumers**
   - Stop accepting new messages from Kafka/RabbitMQ. Complete active job execution up to shutdown deadline (e.g., 30s).
4. **Phase 4: Resource Cleanup**
   - Close database connections, flush OTel trace spans, close log sinks, and exit with code `0`.

---

## 7. Health Check Probes (Kubernetes Model)

Every service MUST expose 3 distinct health endpoints:

| Probe Type | Endpoint Path | Responsibilities | Failure Action |
| :--- | :--- | :--- | :--- |
| **Startup Probe** | `/healthz/startup` | Verifies initial boot, database migrations, model loading. | K8s delays readiness/liveness checks until pass. |
| **Liveness Probe** | `/healthz/liveness` | Verifies process is alive and internal event loop is not deadlocked. Does NOT check external DBs. | K8s restarts container if failed. |
| **Readiness Probe**| `/healthz/readiness`| Verifies service is capable of serving traffic (checks DB, cache, dependency connections). | K8s removes pod from load balancer endpoints if failed. |
