# Cargo Workspace Scaffold Template

## `Cargo.toml` (Root Workspace)

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
authors = ["Engineering Team <engineering@company.com>"]

[workspace.dependencies]
# Async Runtime
tokio = { version = "1.36", features = ["full"] }

# Web Framework & Tower
axum = { version = "0.7", features = ["macros"] }
tower = { version = "0.4", features = ["full"] }
tower-http = { version = "0.5", features = ["trace", "cors", "timeout"] }

# Serialization & Utilities
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
chrono = { version = "0.4", features = ["serde"] }
uuid = { version = "1.7", features = ["v4", "serde"] }

# Error Handling
thiserror = "1.0"
anyhow = "1.0"

# Database & Storage
sqlx = { version = "0.7", features = ["runtime-tokio-native-tls", "postgres", "chrono", "uuid"] }
deadpool-redis = "0.14"

# Observability
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
panic = "abort"
strip = true
```
