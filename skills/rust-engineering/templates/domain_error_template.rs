// Domain Error Handling Template (`thiserror`)
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Entity '{entity}' with ID '{id}' was not found")]
    NotFound { entity: &'static str, id: String },

    #[error("Validation failed: {0}")]
    Validation(String),

    #[error("Conflict condition: {0}")]
    Conflict(String),

    #[error("Database error occurred: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Internal unexpected failure: {0}")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, error_code, message) = match &self {
            AppError::NotFound { entity, id } => (
                StatusCode::NOT_FOUND,
                "NOT_FOUND",
                format!("{} with ID '{}' not found", entity, id),
            ),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, "VALIDATION_ERROR", msg.clone()),
            AppError::Conflict(msg) => (StatusCode::CONFLICT, "CONFLICT", msg.clone()),
            AppError::Database(err) => {
                tracing::error!(error = %err, "Database infrastructure failure");
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "An internal database error occurred".to_string(),
                )
            }
            AppError::Internal(err) => {
                tracing::error!(error = %err, "Internal application error");
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
