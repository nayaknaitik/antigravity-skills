# 05. SDLC, API Evolution, Testing & Code Review Standards

This reference specifies the software engineering lifecycle standards governing testing, code reviews, documentation, versioning, and API evolution.

---

## 1. Testing Pyramid & Verification Strategy

Every production codebase MUST implement an automated multi-tier testing strategy.

```
                  / \
                 /   \     End-to-End & Chaos Tests (5%)
                /-----\
               /       \   Contract & Integration Tests (20%)
              /---------\
             /           \ Unit Tests (70%)
            +-------------+
```

### Testing Tiers & Rules:
1. **Unit Tests (70% Target Coverage)**:
   - Fast, in-memory, deterministic tests.
   - Test domain logic, aggregates, value objects, and application use cases.
   - External dependencies MUST be replaced with mocks or in-memory fakes.
2. **Integration Tests (20%)**:
   - Verify interaction with real backing infrastructure (databases, caches, message brokers).
   - Use containerized environments (Testcontainers / Docker Compose) to test actual SQL queries and migrations.
3. **Contract Tests (5%)**:
   - Consumer-driven contract tests (Pact / OpenAPI validation) ensuring client-server schema compliance without running full E2E environments.
4. **End-to-End & Chaos Testing (5%)**:
   - Automated workflow sanity checks and failure injection (Netflix Chaos Engineering / Chaos Mesh) testing network partitions and pod kills.

---

## 2. Google Code Review Standards

Following Google Engineering Practices, code reviews serve as the primary quality gate for maintainability, security, and knowledge sharing.

### Mandatory Rules for Change Lists (CLs) / Pull Requests (PRs):
1. **Small, Atomic PRs**:
   - Pull Requests SHOULD NOT exceed **400 lines of diff**.
   - Large features MUST be broken down into incremental, flag-guarded PRs.
2. **Clear PR Intent & Context**:
   - Every PR MUST state *Why* the change is being made, *What* changed, and *How* it was verified.
3. **Reviewer Critique Focus**:
   - Reviewers evaluate: Correctness, Architecture, Test coverage, Readability, Security, and Scalability.
   - Non-blocking suggestions must be explicitly prefixed with `Nit:`.
4. **Zero Failing Tests**: No PR may be merged with failing automated build or test pipelines.

---

## 3. API Evolution, Idempotency & Backward Compatibility

APIs are permanent contracts. Stripe's API design philosophy governs API evolution and backward compatibility across our organization.

### Idempotency Keys (Stripe Pattern):
- All non-idempotency HTTP methods (`POST`, `PATCH`) that mutate financial or critical state MUST accept an `Idempotency-Key` header.
- The server records the idempotency key in Redis/DB alongside the response payload.
- Subsequent requests with the same key within 24 hours MUST return the cached response without re-executing the operation.

### Backward Compatibility Rules:
1. **Additive Schema Mutations Only**:
   - New fields added to JSON API requests or responses MUST be optional/nullable.
   - Field names, data types, or existing enum values MUST NOT be renamed or deleted.
2. **API Versioning Strategies**:
   - Use Date-Based Versioning Headers (e.g., `Stripe-Version: 2026-07-23`) or URL path versioning (`/v1/payments`).
   - Deprecate old fields using HTTP `Sunset` headers and warning logs at least 6 months prior to removal.
3. **Protobuf / gRPC Rules**:
   - Field tag numbers MUST NEVER be re-assigned or reused.
   - Mark removed fields as `reserved`.

---

## 4. Semantic Versioning & Package Releases

All software artifacts (libraries, container images, AI skills) conform to **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):

- **MAJOR (X.0.0)**: Incompatible API changes or breaking breaking contracts.
- **MINOR (0.Y.0)**: Backward-compatible functionality addition.
- **PATCH (0.0.Z)**: Backward-compatible bug fixes and security patches.

---

## 5. Documentation & Architectural Decision Records (ADRs)

Documentation is treated as code and lives alongside implementation in revision control.

### Mandatory Docs per Repository:
- `README.md`: Overview, local quickstart, environment variables, build commands.
- `ARCHITECTURE.md`: High-level system diagram, key components, data flow.
- `docs/adr/`: Architecture Decision Records tracking major technical choices using the Nygard template.
- `RUNBOOK.md`: Troubleshooting steps, alert responses, and operational procedures.
