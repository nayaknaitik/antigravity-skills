# User Guide: Rust Engineering Skill

## 1. Overview
The `rust-engineering` skill is a production-grade AI engineering skill designed for building ultra-fast, reliable, memory-safe backend systems, microservices, high-performance networking layers, and distributed systems using Rust and the Tokio async ecosystem.

---

## 2. Activation Triggers
Activate this skill when:
- Designing or writing production Rust crates, web servers (Axum/Tower), or async workloads.
- Structuring Cargo workspaces, module visibility, or domain interfaces.
- Implementing asynchronous task queues, Tokio channel primitives, or cancellation-safe event loops.
- Writing domain error hierarchies (`thiserror`), HTTP status mappers, or logging/tracing setup.
- Optimizing low-level performance, lock-free data structures, atomics, or memory allocators (`mimalloc`).

### Example Prompts:
- *"Scaffold an Axum web service with graceful shutdown and SQLx database pool."*
- *"Build a cancellation-safe Tokio event loop for processing Kafka messages."*
- *"Implement a domain error hierarchy using thiserror with custom HTTP response mapping."*
- *"Design a lock-free atomic sequence counter for sub-microsecond event indexing."*

---

## 3. Core Deliverables
When activated, this skill automatically provides:
1. Production-grade Rust code adhering to API Guidelines and zero-cost abstractions.
2. Clean Cargo workspace layout and dependency management (`Cargo.toml`).
3. Tokio async execution, channel selection, and signal handling (`SIGINT`/`SIGTERM`).
4. Full observability setup (Tracing, OpenTelemetry, Prometheus).
5. Comprehensive unit tests and Criterion benchmark scaffolding.
