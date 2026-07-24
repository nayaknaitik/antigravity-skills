# 02. Go Standard Package Layout & DDD Architecture

This reference defines package structure conventions, Domain-Driven Design (DDD), and Hexagonal Architecture for production Go services.

---

## 1. Standard Go Project Directory Layout

All Go repositories MUST conform to the standard Go application layout:

```
my-go-service/
├── cmd/
│   └── service/
│       └── main.go              <-- Application Entry Point & Composition Root
├── internal/                    <-- Private code (Un-importable outside module)
│   ├── domain/                  <-- Pure Go Domain Models & Value Objects
│   │   ├── order.go
│   │   └── money.go
│   ├── ports/                   <-- Inbound & Outbound Interfaces
│   │   ├── ports.go
│   ├── service/                 <-- Application Use Case Handlers
│   │   └── order_service.go
│   ├── adapters/                <-- Infrastructure Adapters (HTTP, Postgres, Kafka)
│   │   ├── http/
│   │   │   └── order_handler.go
│   │   ├── postgres/
│   │   │   └── order_repository.go
│   │   └── kafka/
│   │       └── event_publisher.go
│   └── config/                  <-- Environment Configuration Structs
│       └── config.go
├── pkg/                         <-- Public shared packages (Internal SDKs)
│   └── telemetry/
├── db/
│   └── migrations/              <-- SQL migration scripts
├── go.mod
├── go.sum
└── Dockerfile
```

---

## 2. Hexagonal Architecture & Interface Placement

In Go, **interfaces belong with the package that uses them (consumer side)**, not the package that implements them.

### Consumer-Side Interface Declaration:
```go
// Location: internal/service/order_service.go
// The application service defines the exact interface it needs from persistence!

type OrderRepository interface {
    Save(ctx context.Context, order *domain.Order) error
    FindByID(ctx context.Context, id uuid.UUID) (*domain.Order, error)
}

type OrderService struct {
    repo OrderRepository
}

func NewOrderService(repo OrderRepository) *OrderService {
    return &OrderService{repo: repo}
}
```

---

## 3. Modular Monolith Architecture in Go

For our organization, Go services should be built as **Modular Monoliths** by default:
- Keep domain boundaries in separate sub-directories under `internal/` (e.g. `internal/trading`, `internal/risk`, `internal/portfolio`).
- Modules interact via explicit Go interfaces or in-process channels.
- Database access between modules is strictly isolated at the table level.
