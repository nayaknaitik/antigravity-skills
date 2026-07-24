# 01. Idiomatic Go, Concurrency & Memory Architecture

This reference defines modern, idiomatic Go engineering standards, concurrency patterns, and memory safety rules synthesized from Effective Go, the Uber Go Style Guide, and Google Go Best Practices.

---

## 1. Core Idiomatic Go & Design Philosophy

Go values **simplicity, readability, and explicit design**. Avoid clever abstractions or dynamic magic.

```
       +-------------------------------------------------------------+
       |                     Go Design Philosophy                    |
       |  • Clear over clever        • Explicit over magic           |
       |  • Accept interfaces        • Return concrete structs       |
       |  • Small, focused interfaces • Never ignore errors          |
       |  • Explicit dependencies    • Zero global mutable state     |
       +-------------------------------------------------------------+
```

### Inviolable Rules of Idiomatic Go:
1. **Interface Segregation ("Go Proverbs")**:
   - Keep interfaces small (1 to 3 methods max).
   - "Accept interfaces, return structs": Callers define interfaces at consumption sites; functions accept interfaces and return concrete struct types or pointers.
2. **Explicit Dependency Wire-Up**:
   - Do NOT use package-level global variables (`var db *sql.DB`) for state.
   - Inject dependencies explicitly via struct constructors (`NewOrderService(repo OrderRepository, logger *slog.Logger)`).
3. **Zero Global Mutexes**: Package state must be instance-scoped.

---

## 2. Concurrency Safety, Goroutines & Context Rules

Goroutines are cheap (2KB initial stack), but leaked goroutines cause fatal memory spikes.

### Goroutine Lifecycle & Leak Prevention:
1. **Never Start a Goroutine Without Knowing How It Stops**:
   - Every goroutine launched with `go func()` MUST be bound to a `context.Context` cancellation or channel drain signal.
2. **Context Propagation**:
   - The first parameter of any IO, database, or RPC function MUST be `ctx context.Context`.
   - Never pass `nil` context; use `context.Background()` or `context.TODO()`.
3. **Timeouts & Deadlines**:
   - Every outbound request MUST derive a context deadline:
     ```go
     ctx, cancel := context.WithTimeout(parentCtx, 2500*time.Millisecond)
     defer cancel() // Mandatory to release resources!
     ```

---

## 3. Concurrency Patterns & Synchronization

### 1. Worker Pool Pattern with Channel Backpressure
```go
type Job struct {
    ID int
}

func WorkerPool(ctx context.Context, workers int, jobs <-chan Job, results chan<- string) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    return
                case job, ok := <-jobs:
                    if !ok {
                        return
                    }
                    results <- fmt.Sprintf("processed job %d", job.ID)
                }
            }
        }()
    }
    wg.Wait()
}
```

### 2. Mutex vs Channel Decision Matrix:
- Use **Channels** for passing ownership of data, coordinating work pipelines, or signaling events.
- Use **`sync.Mutex` / `sync.RWMutex`** for guarding internal in-memory struct state or counter variables.
- Use **`sync/atomic`** for lightweight atomic counter operations (`atomic.AddInt64`).

---

## 4. Graceful Shutdown & Signal Handling

Services MUST catch OS termination signals (`SIGTERM`, `SIGINT`) and shut down gracefully within deadline bounds.

```go
func Run(ctx context.Context) error {
    ctx, stop := signal.NotifyContext(ctx, syscall.SIGTERM, syscall.SIGINT)
    defer stop()

    server := &http.Server{Addr: ":8080", Handler: router}

    go func() {
        if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
            slog.Error("HTTP server error", "error", err)
        }
    }()

    <-ctx.Done() // Wait for SIGTERM/SIGINT
    slog.Info("Shutting down HTTP server...")

    shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    return server.Shutdown(shutdownCtx)
}
```
