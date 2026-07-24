# 01. Architectural Foundations & Design Principles

This reference defines the core architectural paradigms required for production-grade software across all engineering teams and programming languages in our organization.

---

## 1. Clean Architecture & Port-Adapter Pattern (Hexagonal)

Every service must maintain strict decoupling between domain business logic, application orchestration, and infrastructure mechanisms.

```
       +-------------------------------------------------------+
       | Infrastructure Layer (Web, DB, Messaging, CLI)        |
       |  +-------------------------------------------------+  |
       |  | Application Layer (Use Cases, DTOs, Workflows)  |  |
       |  |  +-------------------------------------------+  |  |
       |  |  | Domain Layer (Entities, Value Objects,    |  |  |
       |  |  |               Aggregates, Domain Rules)   |  |  |
       |  |  +-------------------------------------------+  |  |
       |  +-------------------------------------------------+  |
       +-------------------------------------------------------+
```

### Inviolable Rules of Clean Architecture:
1. **The Dependency Rule**: Source code dependencies MUST point inwards towards the Domain. Outer layers depend on inner layers; inner layers MUST NOT depend on outer layers.
2. **Framework Independence**: Domain logic must never inherit from or import third-party web frameworks, ORMs, or IO drivers.
3. **Ports and Adapters**:
   - **Inbound Ports (Primary/Driving)**: Interface definitions for use case invocations (e.g., HTTP handlers, gRPC services, Event Consumers calling Use Case interfaces).
   - **Outbound Ports (Secondary/Driven)**: Interface definitions for external dependencies defined inside the application/domain layer (e.g., `UserRepository`, `PaymentGateway`, `EventPublisher`).
   - **Adapters**: Concrete infrastructure implementations of outbound ports (e.g., `PostgresUserRepository`, `StripeAdapter`, `KafkaEventPublisher`).

---

## 2. SOLID Design Principles

All language-specific codebases must satisfy SOLID principles:

| Principle | Core Requirement | Production Violation Symptom | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **Single Responsibility (SRP)** | A module should have one, and only one, reason to change. | A single handler class handles HTTP routing, database queries, PDF generation, and email sending. | Extract domain services, repositories, and notifications into isolated units. |
| **Open/Closed (OCP)** | Software entities should be open for extension, but closed for modification. | Adding a new payment method requires modifying a 500-line `if/else` chain in `PaymentService`. | Use Strategy Pattern, Polymorphic Dispatch, or Plug-in interfaces. |
| **Liskov Substitution (LSP)** | Subtypes must be substitutable for their base types without altering program correctness. | A subclass overrides a base method to throw `UnsupportedOperationException`. | Segregate interface hierarchies or replace inheritance with composition. |
| **Interface Segregation (ISP)** | Clients should not be forced to depend upon interfaces they do not use. | A lightweight worker service implements a 30-method monolithic CRUD interface. | Break broad interfaces into targeted role-based interfaces (`Reader`, `Writer`, `Payer`). |
| **Dependency Inversion (DIP)** | High-level modules should not depend on low-level modules; both should depend on abstractions. | `UserService` directly instantiates `new PostgresDriver()`. | Inject interfaces into constructors via explicit Dependency Injection container or constructor wire-up. |

---

## 3. Domain-Driven Design (DDD) Core Concepts

For non-trivial business domains, teams must model software around bounded contexts and domain aggregates.

### Core DDD Building Blocks:
- **Ubiquitous Language**: A single, shared vocabulary agreed upon by domain experts and engineers, reflected directly in code variable names, domain types, and API schemas.
- **Bounded Context**: An explicit boundary within which a domain model applies. The meaning of `Customer` in the *Billing Context* differs strictly from `Customer` in the *Fulfillment Context*.
- **Aggregate Root**: A entity cluster that treats state mutations as a single transaction boundary. Access to internal aggregate entities MUST go through the aggregate root.
- **Value Objects**: Immutable objects identified solely by their attributes (e.g., `Money(amount, currency)`, `EmailAddress(string)`), possessing no identity and supporting side-effect-free methods.
- **Domain Events**: Immutable records of significant business events that have occurred in the past (e.g., `OrderPlaced`, `PaymentFailed`). Formatted in past-tense.
- **Repositories**: Abstractions representing in-memory collections for loading and saving Aggregate Roots.

---

## 4. Event-Driven Architecture (EDA) & Messaging

Event-driven microservices must satisfy high-reliability asynchronous communication standards based on Cloudflare, Uber, and Netflix patterns.

### Production Patterns for EDA:
1. **Transactional Outbox Pattern**:
   - State mutations and outward domain events MUST be committed in a single local database transaction.
   - A separate outbox publisher relay polls or streams the outbox table to the event broker (Kafka, RabbitMQ, NATS).
   - *Prevents*: Dual-write failure where database updates succeed but message publishing fails.
2. **Idempotent Consumers**:
   - Message consumers MUST assume **at-least-once delivery**.
   - Consumers must deduplicate messages using a unique `event_id` or business key in an atomic cache/store before processing.
3. **Dead Letter Queues (DLQ) & Retry Exponentials**:
   - Processing failures must retry with exponential backoff and max retry counts (e.g., 3 attempts).
   - Messages exceeding max attempts are automatically routed to a DLQ with original headers and error context attached.
4. **Event Schemas & Backward Compatibility**:
   - All events must conform to standardized CloudEvents specifications.
   - Breaking changes to event payloads are prohibited. Fields may only be added as optional/nullable.

---

## 5. The Twelve-Factor App Standards

Every service deployed to containerized environments (Kubernetes, AWS ECS) must comply with 12-Factor principles:

1. **Codebase**: One codebase tracked in revision control, many deploys.
2. **Dependencies**: Explicitly declare and isolate dependencies (no implicit system-level dependencies).
3. **Config**: Store configuration in the environment (`ENV` variables), strictly separated from code.
4. **Backing Services**: Treat backing resources (databases, queues, caches) as attached resources accessible via URL/credentials.
5. **Build, Release, Run**: Strictly separate build stage (compile), release stage (config + build), and run stage (execution).
6. **Processes**: Execute the app as one or more stateless processes. Persist data in a backing store.
7. **Port Binding**: Export services via port binding (HTTP/gRPC server bound to `$PORT`).
8. **Concurrency**: Scale out via the process model (horizontal scaling of stateless pods).
9. **Disposability**: Maximize robustness with fast startup and graceful shutdown (reacting to `SIGTERM`).
10. **Dev/Prod Parity**: Keep development, staging, and production as similar as possible.
11. **Logs**: Treat logs as event streams piped to `stdout`/`stderr` in JSON format.
12. **Admin Processes**: Run administrative/migration tasks as one-off processes alongside regular app runs.
