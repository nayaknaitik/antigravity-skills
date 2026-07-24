# Lock-Free Concurrency, Memory Ordering & Performance Optimization Reference

## 1. Overview
This reference guide establishes standards for lock-free data structures, atomic memory ordering, micro-benchmarking with Criterion, global memory allocators (`mimalloc`/`jemalloc`), and low-level performance profiling.

---

## 2. Lock-Free Programming & Atomic Memory Ordering

### 2.1 Memory Ordering Cheat Sheet

| Memory Ordering | Hardware Semantics | Recommended Usage |
| :--- | :--- | :--- |
| **`Ordering::Relaxed`** | No synchronization or ordering constraints; only guarantees atomic read/write. | Performance metrics, sequence counters, reference counts non-drop updates. |
| **`Ordering::Acquire`** | Pair with `Release`. Ensures operations *after* the load cannot be reordered before it. | Acquiring a lock, reading shared memory published by another thread. |
| **`Ordering::Release`** | Pair with `Acquire`. Ensures operations *before* the store cannot be reordered after it. | Releasing a lock, publishing data to shared memory. |
| **`Ordering::SeqCst`** | Strict sequential consistency. Globally ordered across all threads. | Default for complex atomic state transitions where thread interleaving is difficult to prove. |

### 2.2 Lock-Free Ring Buffer Blueprint (`AtomicUsize`)
```rust
use std::sync::atomic::{AtomicUsize, Ordering};

pub struct AtomicSequence {
    value: AtomicUsize,
}

impl AtomicSequence {
    pub const fn new(initial: usize) -> Self {
        Self {
            value: AtomicUsize::new(initial),
        }
    }

    pub fn next(&self) -> usize {
        self.value.fetch_add(1, Ordering::Relaxed)
    }

    pub fn get(&self) -> usize {
        self.value.load(Ordering::Acquire)
    }
}
```

---

## 3. High-Performance Mutex Selection

- Avoid `std::sync::Mutex` in performance-critical code due to system call overhead when uncontended.
- Use `parking_lot::Mutex` or `parking_lot::RwLock` for in-memory synchronous critical sections (smaller memory footprint, spin-then-park optimization).
- Use `tokio::sync::Mutex` **ONLY** when lock guards must be held across `.await` points.

---

## 4. Memory Allocator Optimization (`mimalloc` / `jemalloc`)

Default system allocators add lock contention under multi-threaded allocation spikes. Use `mimalloc` or `tikv-jemallocator` in release binaries:

```rust
// main.rs
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

---

## 5. Micro-Benchmarking with Criterion

```rust
// benches/ring_buffer_bench.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use my_crate::AtomicSequence;

fn bench_atomic_sequence(c: &mut Criterion) {
    let seq = AtomicSequence::new(0);
    c.bench_function("atomic_seq_next", |b| {
        b.iter(|| {
            black_box(seq.next());
        })
    });
}

criterion_group!(benches, bench_atomic_sequence);
criterion_main!(benches);
```
