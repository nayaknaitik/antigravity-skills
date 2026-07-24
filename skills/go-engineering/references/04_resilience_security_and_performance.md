# 04. Go Error Handling, Resilience, Security & Low-Latency Performance

This reference details Go error handling paradigms (`errors.Is`, `errors.As`), resilience patterns, OWASP security defaults, and performance profiling.

---

## 1. Go Error Handling Architecture

Go treats errors as **values**. Never ignore returned errors, and never panic except during unrecoverable startup failures.

### Mandatory Rules for Error Handling:
1. **Always Wrap Errors for Context**:
   - Wrap lower-level errors with domain context using `fmt.Errorf("failed to load user %s: %w", userID, err)`.
   - Use `%w` so original error cause can be unwrapped via `errors.Is()` or `errors.As()`.
2. **Sentinel Errors & Domain Error Types**:
   - Export sentinel errors with `Err` prefix (e.g. `var ErrNotFound = errors.New("resource not found")`).
3. **Inspection with `errors.Is` and `errors.As`**:
   ```go
   if errors.Is(err, sql.ErrNoRows) {
       return nil, ErrNotFound
   }

   var netErr net.Error
   if errors.As(err, &netErr) && netErr.Timeout() {
       return nil, ErrTimeout
   }
   ```
4. **Never Swallow Errors**: Either return the error upstream or log it once. NEVER both.

---

## 2. Resilience, Timeouts & Circuit Breakers

### Circuit Breaker with `gobreaker`:
```go
import "github.com/sony/gobreaker"

func NewCircuitBreaker() *gobreaker.CircuitBreaker {
    st := gobreaker.Settings{
        Name:        "PaymentGateway",
        MaxRequests: 5,
        Interval:    10 * time.Second,
        Timeout:     5 * time.Second,
        ReadyToTrip: func(counts gobreaker.Counts) bool {
            failureRatio := float64(counts.TotalFailures) / float64(counts.Requests)
            return counts.Requests >= 10 && failureRatio >= 0.5
        },
    }
    return gobreaker.NewCircuitBreaker(st)
}
```

---

## 3. Low-Latency Performance & `pprof` Profiling

1. **Escape Analysis (`go build -gcflags="-m"`)**:
   - Minimize heap allocations by avoiding returning pointers to short-lived local variables where stack allocation is possible.
2. **Pre-Allocate Slices & Maps**:
   - Always hint capacity for slices and maps when target size is known (`make([]Order, 0, capacity)`).
3. **`pprof` Profiling**: Expose `net/http/pprof` endpoints on internal admin ports for live CPU and memory profiling.
