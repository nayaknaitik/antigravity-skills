// Worked Example: High-Throughput Lock-Free Sequence Counter & Atomic Bus
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

pub struct LockFreeSequenceBus {
    head: AtomicU64,
    tail: AtomicU64,
    capacity: u64,
}

impl LockFreeSequenceBus {
    pub fn new(capacity: u64) -> Self {
        Self {
            head: AtomicU64::new(0),
            tail: AtomicU64::new(0),
            capacity,
        }
    }

    /// Allocates next sequence slot using atomic fetch-add (Lock-Free)
    pub fn publish(&self) -> u64 {
        self.head.fetch_add(1, Ordering::SeqCst)
    }

    /// Reads current published head sequence with Acquire ordering
    pub fn current_head(&self) -> u64 {
        self.head.load(Ordering::Acquire)
    }

    /// Updates processed tail sequence with Release ordering
    pub fn mark_processed(&self, seq: u64) {
        self.tail.store(seq, Ordering::Release);
    }
}

fn main() {
    let bus = Arc::new(LockFreeSequenceBus::new(1024));

    let bus_clone = bus.clone();
    let handle = std::thread::spawn(move || {
        for _ in 0..10_000 {
            let seq = bus_clone.publish();
            bus_clone.mark_processed(seq);
        }
    });

    handle.join().unwrap();
    println!("Final Head Sequence: {}", bus.current_head());
}
