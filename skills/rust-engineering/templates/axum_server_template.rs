// Axum Web Server Production Template
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::net::TcpListener;
use tower_http::trace::TraceLayer;

#[derive(Clone)]
pub struct AppState {
    pub db_pool: sqlx::PgPool,
}

#[derive(Deserialize)]
pub struct CreateItemRequest {
    pub name: String,
}

#[derive(Serialize)]
pub struct ItemResponse {
    pub id: String,
    pub name: String,
}

pub fn app_router(state: AppState) -> Router {
    Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/items", post(create_item))
        .layer(TraceLayer::new_for_http())
        .with_state(state)
}

async fn health_check() -> impl IntoResponse {
    (StatusCode::OK, Json(serde_json::json!({ "status": "UP" })))
}

async fn create_item(
    State(_state): State<AppState>,
    Json(payload): Json<CreateItemRequest>,
) -> impl IntoResponse {
    let response = ItemResponse {
        id: uuid::Uuid::new_v4().to_string(),
        name: payload.name,
    };
    (StatusCode::CREATED, Json(response))
}

pub async fn run_server(addr: SocketAddr, state: AppState) -> Result<(), Box<dyn std::error::Error>> {
    let app = app_router(state);
    let listener = TcpListener::bind(addr).await?;
    tracing::info!("Server listening on http://{}", addr);

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}

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
