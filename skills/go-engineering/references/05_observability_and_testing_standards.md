# 05. Go Observability & Testing Standards

This reference specifies structured logging with `log/slog`, OpenTelemetry distributed tracing, Prometheus metrics, and Table-Driven testing in Go.

---

## 1. Structured Logging with `log/slog` (Go 1.21+)

All logs MUST be output as single-line JSON to `os.Stdout` using Go standard library **`log/slog`**.

### Standard `slog` Initialization & Usage:
```go
func InitLogger() *slog.Logger {
    opts := &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }
    handler := slog.NewJSONHandler(os.Stdout, opts)
    logger := slog.New(handler)
    slog.SetDefault(logger)
    return logger
}

func ProcessOrder(ctx context.Context, logger *slog.Logger, orderID string) {
    logger.InfoContext(ctx, "processing order execution",
        slog.String("order_id", orderID),
        slog.String("trace_id", extractTraceID(ctx)),
    )
}
```

---

## 2. Table-Driven Unit Testing Standards

Go unit tests MUST follow the standard **Table-Driven Test** pattern using standard `testing` package and `testify/assert`.

```go
func TestCalculateFee(t *testing.T) {
    tests := []struct {
        name     string
        amount   decimal.Decimal
        expected decimal.Decimal
        wantErr  bool
    }{
        {
            name:     "valid calculation",
            amount:   decimal.NewFromInt(100),
            expected: decimal.NewFromFloat(0.10),
            wantErr:  false,
        },
        {
            name:     "negative amount error",
            amount:   decimal.NewFromInt(-10),
            expected: decimal.Zero,
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculateFee(tt.amount)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.expected, got)
            }
        })
    }
}
```

---

## 3. Integration Testing with Testcontainers Go

Verify database queries against real PostgreSQL Docker containers during `go test`:

```go
func TestOrderRepositoryIntegration(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    ctx := context.Background()
    pgContainer, err := postgres.RunContainer(ctx,
        testcontainers.WithImage("postgres:16-alpine"),
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("user"),
        postgres.WithPassword("password"),
    )
    require.NoError(t, err)
    t.Cleanup(func() { pgContainer.Terminate(ctx) })

    connStr, _ := pgContainer.ConnectionString(ctx, "sslmode=disable")
    db, err := sql.Open("postgres", connStr)
    require.NoError(t, err)

    // Execute repository tests against live container
}
```
