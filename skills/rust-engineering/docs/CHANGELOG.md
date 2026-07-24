# Changelog: Rust Engineering Skill

## [1.0.0] - 2026-07-23
### Added
- Initial release of production-grade `rust-engineering` AI Skill.
- Cargo workspace scaffolding and dependency inheritance standards.
- Tokio async execution patterns, cancellation safety, and graceful shutdown signal handlers.
- Axum web server and Tower middleware composition templates.
- Error handling patterns (`thiserror` domain errors, `anyhow` application entrypoints, Axum `IntoResponse` status mapping).
- Lock-free concurrency guidelines (`AtomicUsize`, memory ordering `SeqCst`/`Acquire`/`Release`, `parking_lot`).
- Database and storage patterns (SQLx PostgreSQL transactions, Redis connection pooling, Kafka consumers).
- Observability integration (Tracing JSON formatter, OpenTelemetry trace context, Prometheus metrics).
- Unsafe Rust safety rules (`// SAFETY:` comment enforcement, soundness principles, Miri verification).
