# 03. Architecture, DDD & Event-Driven Enterprise Patterns

This reference details Domain-Driven Design (DDD), Clean/Hexagonal Architecture, and Event-Driven messaging patterns in Java.

---

## 1. Hexagonal (Ports & Adapters) Package Structure

To guarantee framework independence and maintainability, packages MUST be organized into explicit layers:

```
com.company.platform.trading/
├── domain/                      <-- Pure Java domain (Zero Framework Dependencies)
│   ├── model/
│   │   ├── Order.java           <-- Aggregate Root
│   │   ├── OrderId.java         <-- Value Object Record
│   │   └── Money.java           <-- Value Object Record
│   ├── port/
│   │   ├── inbound/             <-- Use Case Interfaces
│   │   │   └── CreateOrderUseCase.java
│   │   └── outbound/            <-- Outbound Port Interfaces
│   │       ├── OrderRepositoryPort.java
│   │       └── BrokerPublisherPort.java
│   └── exception/
│       └── InsufficientFundsException.java
├── application/                 <-- Orchestration & Use Case Services
│   └── service/
│       └── CreateOrderService.java
└── infrastructure/              <-- Technical Adapters (Spring, JPA, Kafka, REST)
    ├── adapter/
    │   ├── in/web/              <-- Spring Web REST Controller
    │   │   ├── OrderController.java
    │   │   └── dto/
    │   ├── out/persistence/     <-- Spring Data JPA Repository Adapter
    │   │   ├── OrderEntity.java
    │   │   ├── SpringDataOrderRepository.java
    │   │   └── OrderPersistenceAdapter.java
    │   └── out/messaging/       <-- Kafka Publisher Adapter
    │       └── KafkaBrokerAdapter.java
    └── config/
        └── TradingBeanConfiguration.java
```

---

## 2. Transactional Outbox Pattern with Kafka

Dual writes (updating database + publishing to Kafka) cause catastrophic inconsistency if Kafka publishing fails after DB commit.

### Implementation Protocol:
1. **Outbox Entity**: Create an `outbox` database table within the same transaction boundary as aggregate updates.
2. **Atomic Write**: Write state changes to business tables and append an `OutboxEvent` to the `outbox` table in a single `@Transactional` method.
3. **Outbox Relay (Debezium / Scheduled Poller)**: A background poller reads unprocessed outbox records and publishes them to Kafka, setting `processed_at` timestamp upon acknowledgement.

```java
@Entity
@Table(name = "outbox_events")
public class OutboxEventEntity {
    @Id
    private UUID id;
    private String aggregateType;
    private String aggregateId;
    private String eventType;
    @Column(columnDefinition = "jsonb")
    private String payload;
    private Instant createdAt;
    private Instant processedAt;
}
```

---

## 3. Idempotent Message Consumers

Kafka message consumers MUST assume **at-least-once delivery** and implement idempotent handling:

```java
@KafkaListener(topics = "order-events", groupId = "portfolio-group")
@Transactional
public void consumeOrderEvent(ConsumerRecord<String, String> record) {
    String eventId = extractEventId(record);
    if (processedEventRepository.existsById(eventId)) {
        log.info("Duplicate event received, skipping: {}", eventId);
        return;
    }
    
    // Process business logic
    portfolioService.processOrderEvent(record.value());
    
    // Record processed event key
    processedEventRepository.save(new ProcessedEventEntity(eventId, Instant.now()));
}
```

---

## 4. Saga Pattern for Distributed Transactions

When operations cross bounded contexts or microservices, use the **Saga Pattern** (Orchestration or Choreography based) with explicit compensating transactions (`CancelOrder`, `RefundPayment`) instead of 2-Phase Commit (2PC).
