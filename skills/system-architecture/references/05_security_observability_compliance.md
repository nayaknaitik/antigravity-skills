# Security Architecture, Observability & Compliance Reference

## 1. Overview
This reference guide details security controls, authentication/authorization frameworks, audit logging requirements, regulatory compliance rules, and observability patterns for our financial software platform.

---

## 2. Security Architecture Standards

### 2.1 Identity, Authentication & Authorization (AuthN/AuthZ)
- **Identity Provider (IdP)**: OAuth2.0 / OpenID Connect (OIDC) with mandatory Multi-Factor Authentication (MFA) for trading users.
- **Service-to-Service Security**: Zero-Trust mTLS using SPIFFE/SPIRE or Kubernetes Istio sidecars.
- **Role-Based & Attribute-Based Access Control (RBAC/ABAC)**:
  - Fine-grained permissions: `trading:order:create`, `trading:order:cancel`, `risk:limits:update`, `research:data:read`.
  - ABAC constraints: Enforce asset class restrictions, account maximum trade sizes, and geographic trading permissions.

### 2.2 Secrets Management & Data Encryption
- **Secrets Storage**: HashiCorp Vault or AWS Secrets Manager. Secrets must never be committed to git or stored in plain environment variables.
- **Encryption Standards**:
  - In Transit: TLS 1.3 for all internal and external communication.
  - At Rest: AES-256 for PostgreSQL, ClickHouse, Redis, and Object Storage (S3).
  - API Keys / Exchange Secrets: Hardware Security Module (HSM) or Vault Transit Engine for encrypting venue API keys.

---

## 3. Observability Architecture (The 3 Pillars)

```
[ System Telemetry Sources ]
      │
      ├── OpenTelemetry SDK (Traces & Metrics) ──► OTel Collector ──► Jaeger / Tempo / Prometheus
      │
      └── Structured JSON Logger (Logs)        ──► Vector / FluentBit ──► OpenSearch / Elastic
```

### 3.1 Structured Logging & Financial Audit Trails
- **JSON Format**: Standard fields (`timestamp`, `trace_id`, `span_id`, `service_name`, `level`, `user_id`, `account_id`, `action`, `details`).
- **Audit Logging**: Immutable, tamper-evident audit log for all financial events (`OrderSubmission`, `RiskLimitOverride`, `PositionAdjustment`, `ModelDeployment`). Audit logs must be backed up to read-only S3 buckets with Object Lock (WORM - Write Once Read Many).

### 3.2 Metrics & Golden Signals
- Track 4 Golden Signals across all containers:
  1. **Latency**: Request duration distributions ($p50, p90, p99, p99.9$).
  2. **Traffic**: Requests per second (RPS), FIX messages per second.
  3. **Errors**: 5xx HTTP codes, FIX Session disconnects, Order Rejections.
  4. **Saturation**: CPU, Memory, Queue depth, Connection pool utilization.

### 3.3 Distributed Tracing
- OpenTelemetry instrumentation across API Gateways, OMS services, Risk Engine, and Execution Gateways.
- Trace headers propagated over HTTP (`traceparent`), gRPC metadata, and Kafka record headers (`W3C Trace Context`).

---

## 4. Financial Compliance & Risk Regulatory Requirements

- **MiFID II / SEC Rule 15c3-5**: Pre-trade risk controls and automated kill-switch capabilities.
- **Clock Synchronization (PTP / NTP)**: Timestamp accuracy to within microsecond precision for trade audit logs (IEEE 1588 PTP where required).
- **Recordkeeping**: Retain trade logs, order messages, and risk parameters for 7 years.
