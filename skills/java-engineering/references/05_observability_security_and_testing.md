# 05. Observability, Enterprise Security & Testing Architecture

This reference details structured logging, RFC 7807 error handling, OpenTelemetry observability, and comprehensive automated testing.

---

## 1. RFC 7807 Problem Details Error Handling

All REST API errors MUST return standardized RFC 7807 `application/problem+json` payloads.

### Standard Problem Details Structure:
```json
{
  "type": "https://api.company.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 400,
  "detail": "Account balance of $150.00 is insufficient for order total of $500.00",
  "instance": "/api/v1/orders",
  "timestamp": "2026-07-23T14:30:00Z",
  "code": "ERR_FIN_002",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

### `@ControllerAdvice` Exception Handler Implementation:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InsufficientFundsException.class)
    public ProblemDetail handleInsufficientFunds(InsufficientFundsException ex, HttpServletRequest request) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
        problem.setType(URI.create("https://api.company.com/errors/insufficient-funds"));
        problem.setTitle("Insufficient Funds");
        problem.setProperty("code", "ERR_FIN_002");
        problem.setProperty("timestamp", Instant.now());
        problem.setProperty("trace_id", Tracer.currentTraceId());
        return problem;
    }
}
```

---

## 2. Observability & OpenTelemetry Metrics

### 1. Structured Logback JSON Appender
Logs MUST be formatted as single-line JSON with automatic MDC MDC propagation of `trace_id` and `span_id`.

```xml
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
        <customFields>{"service":"trading-service","environment":"${SPRING_PROFILES_ACTIVE:-default}"}</customFields>
    </encoder>
</appender>
```

### 2. Custom Business Metrics with Micrometer
```java
@Component
public class TradingMetrics {

    private final Counter ordersExecutedCounter;

    public TradingMetrics(MeterRegistry registry) {
        this.ordersExecutedCounter = Counter.builder("trading_orders_executed_total")
            .description("Total executed trading orders")
            .register(registry);
    }

    public void recordOrderExecuted(String orderType) {
        ordersExecutedCounter.increment();
    }
}
```

---

## 3. Comprehensive Automated Testing Strategy

```
                      / \
                     /   \     PIT Mutation & Chaos Tests (5%)
                    /-----\
                   /       \   Testcontainers Integration & ArchUnit (25%)
                  /---------\
                 /           \ JUnit 5 & Mockito Unit Tests (70%)
                +-------------+
```

### 1. Unit Testing (JUnit 5 + Mockito)
- Fast, in-memory tests targeting domain models and use case services.
- Assert invariants using AssertJ (`assertThat(order.getStatus()).isEqualTo(OrderStatus.EXECUTED)`).

### 2. Integration Testing with Testcontainers
Verify database and Kafka persistence against real Docker containers:
```java
@SpringBootTest
@Testcontainers
class OrderRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

### 3. Architecture Verification with ArchUnit
Enforce Clean Architecture boundaries programmatically:
```java
@AnalyzeClasses(packages = "com.company.platform")
public class ArchitectureTest {

    @ArchTest
    public static final ArchRule domainMustNotDependOnSpring =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAPackage("org.springframework..");
}
```
