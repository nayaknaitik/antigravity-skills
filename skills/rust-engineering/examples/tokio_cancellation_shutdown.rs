// Worked Example: Cancellation-Safe Tokio Worker with Graceful Shutdown
use std::time::Duration;
use tokio::sync::mpsc;
use tokio_util::sync::CancellationToken;

pub struct EventPayload {
    pub id: u64,
    pub data: String,
}

pub async fn run_event_processor(
    cancel_token: CancellationToken,
    mut rx: mpsc::Receiver<EventPayload>,
) {
    tracing::info!("Event processor worker started");
    loop {
        tokio::select! {
            // Cancellation branch
            _ = cancel_token.cancelled() => {
                tracing::info!("Received cancellation signal. Draining queue...");
                drain_queue(&mut rx).await;
                tracing::info!("Worker drain complete. Exiting.");
                break;
            }
            // Message processing branch
            maybe_msg = rx.recv() => {
                match maybe_msg {
                    Some(msg) => {
                        process_single_msg(msg).await;
                    }
                    None => {
                        tracing::info!("Channel closed by sender. Worker exiting.");
                        break;
                    }
                }
            }
        }
    }
}

async fn process_single_msg(msg: EventPayload) {
    tracing::debug!(event_id = msg.id, "Processing event");
    tokio::time::sleep(Duration::from_millis(10)).await;
}

async fn drain_queue(rx: &mut mpsc::Receiver<EventPayload>) {
    while let Ok(msg) = rx.try_recv() {
        tracing::info!(event_id = msg.id, "Draining buffered event");
        // Fast sync/light processing during drain
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let (tx, rx) = mpsc::channel::<EventPayload>(100);
    let cancel_token = CancellationToken::new();

    let worker_token = cancel_token.clone();
    let worker_handle = tokio::spawn(run_event_processor(worker_token, rx));

    // Send some events
    for i in 1..=5 {
        tx.send(EventPayload {
            id: i,
            data: format!("Payload {}", i),
        })
        .await?;
    }

    // Trigger graceful shutdown after 100ms
    tokio::time::sleep(Duration::from_millis(100)).await;
    tracing::info!("Triggering global shutdown signal");
    cancel_token.cancel();

    worker_handle.await?;
    Ok(())
}
