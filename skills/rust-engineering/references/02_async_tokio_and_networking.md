# Async Programming, Tokio & High-Performance Networking Reference

## 1. Overview
This reference guide details asynchronous Tokio runtime patterns, Axum web framework integration, Tower middleware composition, channel selection, cancellation safety, and graceful shutdown mechanics.

---

## 2. Tokio Runtime & Task Execution Rules

### 2.1 Multi-Threaded vs Single-Threaded Runtime
- Production HTTP services use multi-threaded runtime: `#[tokio::main]`.
- CPU-intensive tasks MUST NOT run directly on async worker threads (causes event loop starvation).
- Use `tokio::task::spawn_blocking` for blocking I/O or heavy CPU computations (e.g., password hashing, synchronous cryptography).

```rust
// Correct: Offload CPU-heavy work
let hashed_password = tokio::task::spawn_blocking(move || {
    bcrypt::hash(password, 12)
}).await??;
```

### 2.2 Tokio Channel Selection Matrix

| Channel Type | Primitive | Typical Use Case |
| :--- | :--- | :--- |
| **mpsc** (Multi-Producer, Single-Consumer) | `tokio::sync::mpsc` | Command queues, task dispatching, database write queues |
| **oneshot** (Single-Producer, Single-Consumer) | `tokio::sync::oneshot` | RPC request-response response pairing |
| **broadcast** (Multi-Producer, Multi-Consumer) | `tokio::sync::broadcast` | Event bus, market data tick distribution to web sockets |
| **watch** (Single-Producer, Multi-Consumer) | `tokio::sync::watch` | Configuration updates, service status, cancellation signals |

---

## 3. Cancellation Safety & `tokio::select!`

### 3.1 What is Cancellation Safety?
When a `tokio::select!` branch loses, its underlying `Future` is dropped. If the future held intermediate state across an `.await` boundary (e.g. reading half a socket payload or updating a buffer), that state is lost.

### 3.2 Cancellation-Safe Primitives
- `tokio::sync::mpsc::Receiver::recv` (Safe)
- `tokio::net::TcpStream::read` (Unsafe - partial read dropped)
- `tokio::io::AsyncReadExt::read_buf` (Unsafe - use explicit buffer management)

```rust
// Safe Select Loop pattern with CancellationToken
use tokio_util::sync::CancellationToken;

pub async fn run_worker(cancel: CancellationToken, mut rx: mpsc::Receiver<Task>) {
    loop {
        tokio::select! {
            _ = cancel.cancelled() => {
                tracing::info!("Worker cancellation signal received, draining queue...");
                break;
            }
            Some(task) = rx.recv() => {
                process_task(task).await;
            }
        }
    }
}
```

---

## 4. Axum & Tower Web Stack Architecture

### 4.1 Production Axum Architecture
- Explicit Application State (`Axum::extract::State`).
- Type-safe Extractors (`Json<T>`, `Path<T>`, `Query<T>`).
- Tower Middleware Layering (`TimeoutLayer`, `TraceLayer`, `CorsLayer`, `ConcurrencyLimitLayer`).

```rust
use axum::{routing::get, routing::post, Router, extract::State};
use tower_http::trace::TraceLayer;
use std::sync::Arc;

#[derive(Clone)]
pub struct AppState {
    pub db_pool: sqlx::PgPool,
}

pub fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/users", post(create_user))
        .layer(TraceLayer::new_for_http())
        .with_state(state)
}
```

---

## 5. Graceful Shutdown & Signal Handling

Always implement graceful shutdown handling `SIGINT` (Ctrl+C) and `SIGTERM` (Kubernetes termination signal):

```rust
async fn shutdown_signal() {
    let ctrl_c = async {
        tokio::signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
    tracing::info!("Shutdown signal received, initiating graceful shutdown...");
}
```
