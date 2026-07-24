# 03. Architecture, API & Database Review Standards

This reference specifies review procedures for architectural layering, API contracts, idempotency, and database performance.

---

## 1. Architectural Layering & SOLID Review

### 1. Inward Dependency Rule:
- Verify that domain logic does NOT import third-party web frameworks (Spring Web, Chi, Gin, Express), ORMs (Hibernate, GORM), or database drivers.
- Dependencies MUST point inwards toward domain models.

### 2. SOLID Verification:
- **SRP**: Flag classes/packages performing HTTP handling, business calculations, SQL queries, and email sending simultaneously.
- **DIP**: Flag direct instantiation of low-level infrastructure drivers inside use case services; enforce interface injection.

---

## 2. API Contract & Idempotency Audit

### 1. Idempotency Keys (Stripe Standard):
- All non-idempotent HTTP methods (`POST`, `PATCH`) mutating state MUST require an `Idempotency-Key` header.
- Cached idempotency responses MUST be returned on duplicate requests within 24 hours.

### 2. Backward Compatibility:
- **BLOCKER**: Removing or renaming existing fields in API request/response schemas is strictly prohibited.
- New fields MUST be optional/nullable.

---

## 3. Database Performance & Persistence Audit

### 1. N+1 Query Prevention:
- Flag any query loading child entities inside a loop.
- Require `JOIN FETCH` (JPA/Hibernate) or explicit batch loading (`sqlc` / SQL).

### 2. Connection Pool & Timeouts:
- Database query execution MUST be bounded by context/query timeouts.
- Connection pools MUST define explicit `MaxOpenConns` / `max-active` parameters.

### 3. Database Migrations (Flyway / Liquibase / golang-migrate):
- Schema modifications MUST be executed via versioned migration SQL scripts. Auto-update DDL options in ORMs MUST be disabled.
