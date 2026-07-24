# Error Handling, Custom Error Hierarchies & Context Reference

## 1. Overview
This reference guide details Rust error handling best practices, differentiating between domain errors (`thiserror`), application entrypoint errors (`anyhow`), diagnostic reporting (`miette`/`snafu`), and HTTP status mapping.

---

## 2. The `thiserror` vs `anyhow` Paradigm

| Error Library | Recommended Location | Rationale & Characteristics |
| :--- | :--- | :--- |
| **`thiserror`** | Libraries, Domain Crates, Core Services | Defines strongly-typed, enum-based error hierarchies. Provides zero allocation costs, static dispatch, and `#[error(...)]` formatting annotations. |
| **`anyhow`** | Binary Entrypoints (`main.rs`), CLI applications, Integration Tests | Opaque error wrapper (`anyhow::Error`) holding dynamic error context via `.context("failed to execute operation")`. Convenient for top-level error propagation where callers do not pattern match errors. |

---

## 3. Production Domain Error Pattern (`thiserror`)

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum OrderDomainError {
    #[error("Order '{0}' not found")]
    NotFound(String),

    #[error("Insufficient margin for account '{account_id}': required {required}, available {available}")]
    InsufficientMargin {
        account_id: String,
        required: f64,
        available: f64,
    },

    #[error("Database error occurred: {0}")]
    DatabaseError(#[from] sqlx::Error),

    #[error("Internal infrastructure failure: {0}")]
    Internal(#[source] anyhow::Error),
}
```

---

## 4. Axum HTTP Error Response Mapping Pattern

Implement `IntoResponse` for custom domain error types to automatically map domain errors to HTTP response codes with structured JSON bodies:

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

impl IntoResponse for OrderDomainError {
    fn into_response(self) -> Response {
        let (status, error_code, message) = match &self {
            OrderDomainError::NotFound(id) => (
                StatusCode::NOT_FOUND,
                "ORDER_NOT_FOUND",
                format!("Order '{}' was not found", id),
            ),
            OrderDomainError::InsufficientMargin { account_id, .. } => (
                StatusCode::UNPROCESSABLE_ENTITY,
                "INSUFFICIENT_MARGIN",
                format!("Insufficient margin for account '{}'", account_id),
            ),
            OrderDomainError::DatabaseError(err) => {
                tracing::error!(error = %err, "Database infrastructure error");
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "An internal database error occurred".to_string(),
                )
            }
            OrderDomainError::Internal(err) => {
                tracing::error!(error = %err, "Internal domain error");
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "An unexpected error occurred".to_string(),
                )
            }
        };

        let body = Json(json!({
            "error": {
                "code": error_code,
                "message": message
            }
        }));

        (status, body).into_response()
    }
}
```
