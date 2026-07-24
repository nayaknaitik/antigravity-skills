# 01. Java 21+ Modern Language Features & Concurrency Architecture

This reference defines modern Java 21+ idioms, Virtual Threads (Project Loom), pattern matching, records, sealed interfaces, and memory-safe concurrency standards for enterprise financial and AI systems.

---

## 1. Virtual Threads (Project Loom) & Concurrency Paradigm

Java 21 introduces **Virtual Threads** (`Thread.ofVirtual()`), providing lightweight, user-mode threads managed by the Java runtime rather than 1:1 OS threads.

```
       +-------------------------------------------------------------+
       |                  100,000+ Virtual Threads                   |
       +-------------------------------------------------------------+
                                     |  (Mounted dynamically)
                                     v
       +-------------------------------------------------------------+
       |   ForkJoinPool Carrier Threads (Equal to CPU core count)    |
       +-------------------------------------------------------------+
                                     |
                                     v
       +-------------------------------------------------------------+
       |                      Operating System                       |
       +-------------------------------------------------------------+
```

### Inviolable Rules for Virtual Threads:
1. **Never Pool Virtual Threads**: Virtual threads are cheap to create (~1KB footprint) and short-lived. Never wrap Virtual Threads in a fixed-size `ExecutorService` thread pool. Create a new virtual thread per task (`Executors.newVirtualThreadPerTaskExecutor()`).
2. **Avoid Pinning Carrier Threads**:
   - Carrier threads become pinned when executing inside `synchronized` blocks/methods containing blocking IO.
   - *Remediation*: Replace `synchronized` blocks performing IO with `java.util.concurrent.locks.ReentrantLock`.
3. **Structured Concurrency**:
   - Use `StructuredTaskScope` (Preview feature in Java 21+) to treat groups of concurrent tasks executed in sub-threads as a single unit of work.
   - Guarantees thread cancellation and exception propagation when sub-tasks fail.

### Virtual Threads Configuration in Spring Boot 3.2+:
```yaml
spring:
  threads:
    virtual:
      enabled: true # Automatically configures Tomcat and @Async to use Virtual Threads
```

---

## 2. Java Records, Value Objects & Data Immutability

Records are transparent data carriers with built-in immutability, `equals()`, `hashCode()`, and `toString()`.

### Best Practices for Records:
1. **Use Records for DTOs, Value Objects, and Commands**: All API request/response bodies, domain value objects, and asynchronous command payloads MUST be declared as `record`.
2. **Compact Constructor Validation**: Perform defensive invariant validation inside compact constructors.
   ```java
   public record Money(BigDecimal amount, Currency currency) {
       public Money {
           Objects.requireNonNull(amount, "amount must not be null");
           Objects.requireNonNull(currency, "currency must not be null");
           if (amount.compareTo(BigDecimal.ZERO) < 0) {
               throw new IllegalArgumentException("amount cannot be negative");
           }
       }
   }
   ```
3. **Immutability of Collections**: Defensive copies MUST be made when passing collections to record constructors (`List.copyOf(items)`).

---

## 3. Sealed Classes & Domain Type Exhaustiveness

Sealed classes/interfaces constrain which classes may extend or implement them, enabling exhaustive compile-time pattern matching.

### Domain State Modeling Example:
```java
public sealed interface OrderState permits DraftState, SubmittedState, ExecutedState, CancelledState {}

public record DraftState(LocalDateTime createdAt) implements OrderState {}
public record SubmittedState(LocalDateTime submittedAt, String brokerId) implements OrderState {}
public record ExecutedState(LocalDateTime executedAt, BigDecimal fillPrice) implements OrderState {}
public record CancelledState(LocalDateTime cancelledAt, String reason) implements OrderState {}
```

### Exhaustive Switch Expression (Zero Default Branch Required):
```java
public String processOrderState(OrderState state) {
    return switch (state) {
        case DraftState d -> "Draft created at " + d.createdAt();
        case SubmittedState s -> "Submitted to broker " + s.brokerId();
        case ExecutedState e -> "Executed at price " + e.fillPrice();
        case CancelledState c -> "Cancelled: " + c.reason();
    }; // Compiler errors if any permitted type is unhandled!
}
```

---

## 4. Record Patterns & Pattern Matching

Java 21 supports deep deconstruction pattern matching for records.

```java
public BigDecimal calculateFee(Object event) {
    if (event instanceof TradeExecutedEvent(String orderId, Money(BigDecimal amount, Currency curr))) {
        return amount.multiply(new BigDecimal("0.001"));
    }
    return BigDecimal.ZERO;
}
```

---

## 5. Optional Idioms & Null Safety

1. **Never Return Null**: Methods returning collections MUST return empty collections (`List.of()`, `Collections.emptyList()`), never `null`.
2. **Optional Returns Only**: Use `Optional<T>` exclusively for method return types where a non-collection value may be absent.
3. **Prohibited Optional Uses**:
   - DO NOT use `Optional` for class fields, record fields, or method parameter types.
   - DO NOT call `optional.get()` without `isPresent()` verification; prefer `optional.orElseThrow()`, `optional.map()`, or `optional.ifPresent()`.
