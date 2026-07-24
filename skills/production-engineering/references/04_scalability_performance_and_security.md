# 04. Scalability, Performance, Dependency Injection & Security

This reference defines organization-wide standards for horizontal scalability, performance optimization, dependency management, configuration, and security.

---

## 1. Scalability Architecture

To support massive throughput and zero-downtime operations (Stripe / Cloudflare architecture), services must adhere to scalability patterns:

### Mandatory Rules:
1. **Stateless Service Process**: Application nodes MUST NOT hold in-memory user sessions or state between requests. Shared state MUST reside in Redis, PostgreSQL, or S3.
2. **Database Read/Write Separation**: Heavy read queries MUST be directed to read-replicas. Write operations MUST execute on the primary DB node within transactional boundaries.
3. **Connection Pooling**: Database connections MUST be managed via explicit, sized connection pools (e.g., Min: 5, Max: 20 connections per pod) with connection lifetime bounds.
4. **Caching Strategy**:
   - **Cache-Aside Pattern**: Read from cache first; on miss, query database, store result in cache with explicit TTL.
   - **Cache Stampede Protection**: Use single-flight or distributed locks when updating hot cache keys.
   - **Mandatory TTL**: Every cached item MUST have an explicit Time-To-Live (TTL).

---

## 2. Performance Engineering Standards

### Latency Budgeting & P99 SLAs:
Services must meet defined service-level objectives (SLOs) for P95 and P99 latency:
- **P95 Latency**: `< 100ms`
- **P99 Latency**: `< 250ms`

### High Performance Guidelines:
- **Async IO / Non-Blocking Execution**: Use non-blocking IO event loops (Tokio in Rust, Go goroutines, Netty in Java, Node.js event loop) for network operations.
- **Resource Allocations**: Explicitly define Kubernetes container CPU/Memory requests and limits:
  ```yaml
  resources:
    requests:
      cpu: "250m"
      memory: "512Mi"
    limits:
      cpu: "1000m"
      memory: "1Gi"
  ```
- **Garbage Collection Optimization**: Avoid short-lived object allocation inside hot loops.

---

## 3. Dependency Injection & Inversion of Control

Dependency Injection (DI) ensures clean separation between object construction and business execution.

### Principles:
1. **Constructor Injection**: Dependencies MUST be passed explicitly via object constructors or factory functions. Field or magic global injection is prohibited.
2. **Inject Interfaces, Not Concrete Structs**: Depend on outbound ports (interfaces), enabling seamless replacement with mock or fake implementations during testing.
3. **Deterministic Composition Root**: All dependencies, singletons, and wire-ups MUST be initialized explicitly at application startup in a single main/wire composition function.

---

## 4. Configuration Management & Feature Flags

### Configuration Rules:
1. **Strongly-Typed Configuration**: Convert raw environment variables into a strongly-typed configuration struct during boot.
2. **Fail Fast on Invalid Config**: Validate all required config keys and formats at startup. If validation fails, exit immediately with non-zero status.
3. **Feature Flags**: Dynamic behavior changes must be guarded by feature flags (e.g., LaunchDarkly or Redis flags) without requiring service redeployment.

---

## 5. Security & Secrets Management Standards

Security must follow Microsoft Security Development Lifecycle (SDL) and OWASP Top 10 guidelines.

### Secrets Management:
1. **Zero Hardcoded Secrets**: Passwords, API keys, private keys, and connection strings MUST NEVER be committed to version control.
2. **Secrets Vault Integration**: Fetch secrets dynamically at runtime or inject via Kubernetes Secrets from HashiCorp Vault / AWS Secrets Manager.
3. **Automated Scanning**: CI/CD pipelines MUST execute secret scanning tools (`trufflehog`, `gitleaks`) on every pull request.

### Application Security Rules:
- **TLS Everywhere**: All internal and external network traffic MUST use TLS 1.3 / mTLS (Istio service mesh).
- **Least Privilege**: Application database credentials must only possess required DML privileges (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) and NOT `DROP` or `ALTER` schema privileges.
- **Input Sanitization**: Validate and sanitize all external user input against strict typed schemas to eliminate SQL injection, XSS, and command injection vulnerabilities.
- **Authentication & Authorization**: Enforce JWT / OAuth2 validation on every inbound request at API gateways and service boundaries.
