# Database, Messaging & Observability Reference

## 1. Overview
This reference guide details production patterns for SQLx PostgreSQL connection pooling, Redis caching, Kafka async streaming, and OpenTelemetry observability setup.

---

## 2. SQLx PostgreSQL Integration Patterns

### 2.1 Connection Pool Setup
```rust
use sqlx::postgres::PgPoolOptions;
use std::time::Duration;

pub async fn create_db_pool(database_url: &str) -> Result<sqlx::PgPool, sqlx::Error> {
    PgPoolOptions::new()
        .max_connections(50)
        .min_connections(10)
        .acquire_timeout(Duration::from_secs(3))
        .idle_timeout(Duration::from_secs(600))
        .max_lifetime(Duration::from_secs(1800))
        .connect(database_url)
        .await
}
```

### 2.2 Compile-Time Verified Queries & Transactions
```rust
pub async fn update_user_balance(
    tx: &mut sqlx::Transaction<'_, sqlx::Postgres>,
    user_id: uuid::Uuid,
    amount: f64,
) -> Result<(), sqlx::Error> {
    sqlx::query!(
        r#"
        UPDATE accounts
        SET balance = balance + $1, updated_at = NOW()
        WHERE user_id = $2
        "#,
        amount,
        user_id
    )
    .execute(&mut **tx)
    .await?;
    
    Ok(())
}
```

---

## 3. Redis Caching & Connection Management

```rust
use deadpool_redis::{Config, Pool, Runtime};

pub fn create_redis_pool(redis_url: &str) -> Pool {
    let cfg = Config::from_url(redis_url);
    cfg.create_pool(Some(Runtime::Tokio1)).unwrap()
}
```

---

## 4. OpenTelemetry & Prometheus Tracing Setup

```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter, Registry};

pub fn init_telemetry() {
    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info,my_backend=debug"));

    let formatting_layer = tracing_subscriber::fmt::layer()
        .json()
        .with_current_span(true)
        .with_span_list(true);

    Registry::default()
        .with(env_filter)
        .with(formatting_layer)
        .init();
}
```
