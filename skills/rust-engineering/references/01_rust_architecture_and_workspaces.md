# Rust Architecture, Cargo Workspaces & Module Design Reference

## 1. Overview
This reference guide establishes organizational standards for structuring production Rust projects, Cargo workspaces, module visibility, dependency management, and type system usage.

---

## 2. Cargo Workspace Architecture

For production systems, prefer a **Cargo Workspace** dividing the application into isolated, single-responsibility crates.

```
my-backend/
├── Cargo.toml                  # Root workspace manifest with inherited dependencies
├── Cargo.lock
├── crates/
│   ├── api/                    # Axum web server, HTTP routing, DTOs, extractors
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── domain/                 # Pure domain models, business logic, error types, traits
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── infra/                  # Database implementations (SQLx), Kafka, Redis, gRPC
│   │   ├── Cargo.toml
│   │   └── src/
│   └── common/                 # Telemetry, configuration, shared utilities
│       ├── Cargo.toml
│       └── src/
```

### Root `Cargo.toml` Best Practices:
```toml
[workspace]
resolver = "2"
members = [
    "crates/api",
    "crates/domain",
    "crates/infra",
    "crates/common",
]

[workspace.package]
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
license = "MIT OR Apache-2.0"

[workspace.dependencies]
# Standard async stack
tokio = { version = "1.36", features = ["full"] }
axum = { version = "0.7", features = ["macros"] }
tower = { version = "0.4", features = ["full"] }
tower-http = { version = "0.5", features = ["trace", "cors", "timeout"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
thiserror = "1.0"
anyhow = "1.0"
sqlx = { version = "0.7", features = ["runtime-tokio-native-tls", "postgres", "chrono", "uuid"] }

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
panic = "abort"
strip = true
```

---

## 3. Module Visibility & Encapsulation

1. **Keep Items Private by Default**: Use `pub(crate)` for internal crate items. Only expose `pub` on root public interfaces.
2. **Re-export Clean API Surfaces**:
   ```rust
   // lib.rs
   mod internal_impl;
   
   pub use internal_impl::PublicService;
   ```
3. **Encapsulate Internal Mutability**: Wrap shared mutable state inside domain types (`Arc<Mutex<T>>` or `Arc<RwLock<T>>` or atomic fields), keeping locks private.

---

## 4. Traits, Generics & Dynamic Dispatch Guidelines

| Paradigm | Usage Criteria | Code Example |
| :--- | :--- | :--- |
| **Static Dispatch (`impl Trait` / Generics)** | High-frequency execution paths, performance-critical loops where monomorphization and inlining provide zero overhead. | `fn process<R: Repository>(repo: &R)` |
| **Dynamic Dispatch (`Box<dyn Trait>` / `&dyn Trait`)** | Plugin architectures, heterogeneous collections, or reducing binary code bloat where virtual method call cost ($\sim 1\text{-}3\text{ns}$) is negligible compared to network/IO latency. | `pub type DynOrderRepo = Arc<dyn OrderRepository + Send + Sync>;` |

### Async Traits Pattern:
Using native `async fn` in traits (Rust 1.75+):
```rust
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, DomainError>;
    async fn save(&self, user: &User) -> Result<(), DomainError>;
}
```

---

## 5. Ownership, RAII & Lifetime Management

1. **RAII (Resource Acquisition Is Initialization)**: Use Rust's `Drop` trait for deterministic cleanup of database connections, sockets, or lock guards.
2. **Avoid Unnecessary Clones**: Prefer borrowing (`&str`, `&[u8]`) or zero-copy types (`bytes::Bytes`, `Arc<T>`) for heavy payloads.
3. **Explicit Lifetime Annotations**: Keep lifetime parameter names short (`'a`) and clear. Avoid elision when it obfuscates API contracts.
