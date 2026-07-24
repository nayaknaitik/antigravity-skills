# 03. Go Persistence, Messaging & Cloud Native Standards

This reference specifies database persistence, SQL generation (`sqlc`), connection pooling, Redis caching, and Kafka/NATS event messaging in Go.

---

## 1. Type-Safe SQL Persistence (`database/sql` & `sqlc`)

Prefer **`sqlc`** or **`sqlx`** over heavy ORMs for transparent, high-performance database interaction in Go.

### 1. `sqlc` Query Definition (`db/queries/orders.sql`):
```sql
-- name: CreateOrder :one
INSERT INTO orders (id, account_id, symbol, side, price, quantity, status, created_at)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
RETURNING id, account_id, symbol, side, price, quantity, status, created_at;

-- name: GetOrderByID :one
SELECT id, account_id, symbol, side, price, quantity, status, created_at
FROM orders
WHERE id = $1;
```

### 2. Connection Pool Tuning:
```go
func NewPostgresDB(cfg DBConfig) (*sql.DB, error) {
    db, err := sql.Open("postgres", cfg.DSN)
    if err != nil {
        return nil, fmt.Errorf("failed to open db connection: %w", err)
    }

    db.SetMaxOpenConns(25)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(15 * time.Minute)
    db.SetConnMaxIdleTime(5 * time.Minute)

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := db.PingContext(ctx); err != nil {
        return nil, fmt.Errorf("failed to ping db: %w", err)
    }
    return db, nil
}
```

---

## 2. Transactional Outbox Pattern in Go

When publishing domain events to Kafka or NATS, execute database state updates and outbox message insertions within a single `*sql.Tx`.

```go
func (r *OrderPostgresRepo) CreateWithOutbox(ctx context.Context, order *domain.Order, event *domain.Event) error {
    tx, err := r.db.BeginTx(ctx, nil)
    if err != nil {
        return fmt.Errorf("failed to begin tx: %w", err)
    }
    defer tx.Rollback()

    // 1. Insert Order
    _, err = tx.ExecContext(ctx, insertOrderQuery, order.ID, order.AccountId, order.Symbol)
    if err != nil {
        return fmt.Errorf("failed to insert order: %w", err)
    }

    // 2. Insert Outbox Event
    payloadBytes, _ := json.Marshal(event.Payload)
    _, err = tx.ExecContext(ctx, insertOutboxQuery, event.ID, event.Type, payloadBytes, time.Now())
    if err != nil {
        return fmt.Errorf("failed to insert outbox event: %w", err)
    }

    return tx.Commit()
}
```

---

## 3. High-Performance HTTP Routers (Chi Router)

Use lightweight, idiomatic routers like **Chi** (`github.com/go-chi/chi/v5`) for REST APIs:

```go
func NewRouter(handler *OrderHandler) http.Handler {
    r := chi.NewRouter()
    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.Timeout(60 * time.Second))

    r.Route("/api/v1/orders", func(r chi.Router) {
        r.Post("/", handler.CreateOrder)
        r.Get("/{id}", handler.GetOrder)
    })
    return r
}
```
