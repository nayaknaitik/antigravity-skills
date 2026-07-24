# 04. Resilience, Persistence & High Performance Standards

This reference specifies standards for fault tolerance, JPA/Hibernate performance, database migrations, and Redis caching.

---

## 1. Resilience4j & Rate Limiting (Bucket4j)

All outbound external network calls MUST be guarded by **Resilience4j** instances.

### Resilience4j Declarative Configuration:
```yaml
resilience4j:
  circuitbreaker:
    instances:
      brokerService:
        slidingWindowType: COUNT_BASED
        slidingWindowSize: 100
        minimumNumberOfCalls: 20
        failureRateThreshold: 50
        waitDurationInOpenState: 5s
        permittedNumberOfCallsInHalfOpenState: 10
  retry:
    instances:
      brokerService:
        maxAttempts: 3
        waitDuration: 100ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2.0
        retryExceptions:
          - java.io.IOException
          - org.springframework.web.client.ResourceAccessException
```

### Rate Limiting with Bucket4j & Redis:
Protect sensitive financial and trading endpoints using Bucket4j rate limiters:
```java
public boolean isAllowed(String apiKey) {
    Bucket bucket = bucketByName(apiKey);
    return bucket.tryConsume(1);
}
```

---

## 2. JPA & Hibernate High-Performance Persistence Rules

### 1. N+1 Query Problem Prevention
- NEVER rely on default fetch types for `@OneToMany` or `@ManyToMany` (default is `LAZY`).
- Use explicit `JOIN FETCH` inside JPQL/HQL queries or Spring Data `@EntityGraph` for queries retrieving associated collections.

```java
@Query("SELECT o FROM OrderEntity o JOIN FETCH o.items WHERE o.customer.id = :customerId")
List<OrderEntity> findOrdersWithItemsByCustomerId(@Param("customerId") UUID customerId);
```

### 2. Optimistic & Pessimistic Locking
- High-concurrency entities mutating balance or inventory MUST use Optimistic Locking (`@Version` long version).
- Critical financial transactions requiring exclusive locks MUST use Pessimistic Write Locking (`LockModeType.PESSIMISTIC_WRITE`).

### 3. Database Migration Standards (Flyway)
- Schema changes MUST be executed via versioned Flyway migration SQL scripts located in `src/main/resources/db/migration/`.
- Filename format: `V{MAJOR}.{MINOR}.{PATCH}__{Description}.sql` (e.g. `V1.0.1__create_orders_table.sql`).
- Hibernate DDL auto-generation (`spring.jpa.hibernate.ddl-auto=update`) is STRICTLY PROHIBITED in production environments.

---

## 3. Redis Caching & Cache-Aside Pattern

```java
@Service
public class PortfolioService {

    @Cacheable(value = "portfolios", key = "#portfolioId", unless = "#result == null")
    public PortfolioResponse getPortfolioById(UUID portfolioId) {
        return portfolioRepository.findById(portfolioId)
            .map(portfolioMapper::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("Portfolio not found: " + portfolioId));
    }
}
```

- Mandatory TTL: Every Redis key MUST have an explicit expiration time configured via `RedisCacheManager`.
- Cache Stampede: Use SingleFlight locks or Redis Mutex when recalculating heavy cache entries.
