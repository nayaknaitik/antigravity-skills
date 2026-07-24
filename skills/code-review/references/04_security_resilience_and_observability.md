# 04. Security, Resilience & Observability Review Standards

This reference specifies audit procedures for OWASP Top 10 security vulnerabilities, resilience policies, and OpenTelemetry instrumentation.

---

## 1. Security & OWASP Top 10 Audit

### 1. Zero Hardcoded Secrets:
- **CRITICAL BLOCKER**: Hardcoded passwords, API tokens, JWT secrets, or private keys committed in source code MUST cause an immediate review rejection (`REJECTED`).
- Secrets MUST be loaded dynamically from environment variables or external vaults (Vault, AWS Secrets Manager).

### 2. SQL Injection & Input Validation:
- Flag string concatenation inside SQL queries (`"SELECT * FROM users WHERE name = '" + name + "'"`). Parameterized queries are mandatory.

### 3. TLS & Auth Isolation:
- Verify that endpoints enforce TLS 1.3 / mTLS and authenticate requests via JWT/OAuth2 headers.

---

## 2. Resilience & Graceful Degradation Audit

1. **Explicit Network Timeouts**: Every outbound network call MUST have a configured execution timeout.
2. **Retries with Full Jitter**: Retries MUST apply full randomized jitter to prevent thundering herd spikes.
3. **Circuit Breakers**: Fragile external dependencies MUST be protected by circuit breakers.
4. **Graceful Shutdown**: Applications MUST handle `SIGTERM` signals and drain traffic prior to exit.

---

## 3. Observability & Telemetry Audit

1. **Structured JSON Logs**: Plain text `System.out.println` or `fmt.Println` logging is PROHIBITED. Logs MUST be structured JSON to `stdout`.
2. **Trace Context Correlation**: Logs MUST include `trace_id` and `span_id` fields.
3. **Prohibited Log Data**: PII (credit cards, passwords, SSNs) MUST NOT be logged.
