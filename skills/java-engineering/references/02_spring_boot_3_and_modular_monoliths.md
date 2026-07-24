# 02. Spring Boot 3+ & Spring Modulith Architecture

This reference defines standards for building enterprise backend platforms using Spring Boot 3+ and Spring Modulith in accordance with our modular monolith philosophy.

---

## 1. Modular Monolith Architectural Philosophy

Our organization prefers **Modular Monoliths** over microservices by default. A modular monolith enforces strict architectural boundaries inside a single deployment unit, eliminating network overhead while preserving domain decoupling.

```
       +-------------------------------------------------------------+
       |               Spring Boot 3 Application                     |
       |  +---------------------+   Events    +-------------------+  |
       |  |  Portfolio Module   | ----------> |   Order Module    |  |
       |  |  (Spring Modulith)  |             | (Spring Modulith) |  |
       |  +---------------------+             +-------------------+  |
       |             |                                 |             |
       |             v                                 v             |
       |  +-------------------------------------------------------+  |
       |  |        PostgreSQL Database (Isolated Schemas)         |  |
       |  +-------------------------------------------------------+  |
       +-------------------------------------------------------------+
```

### Spring Modulith Rules:
1. **Module Package Encapsulation**: Top-level packages under the application root represent independent domain modules (e.g. `com.company.platform.portfolio`, `com.company.platform.order`).
2. **Package Visibility**: Only classes inside the root module package are accessible across module boundaries. Internal implementation packages (`internal`, `infrastructure`) MUST be package-private.
3. **Cross-Module Invocations**: Modules MUST communicate via Spring Application Events or explicitly exposed Java interfaces. Direct database joins across module boundaries are prohibited.
4. **Architectural Verification**: Every module structure MUST be verified using `ApplicationModules.of(Application.class).verify()`.

---

## 2. Spring Boot 3 Configuration & Profiles

### 1. Strongly-Typed `@ConfigurationProperties`
Environment configuration MUST be bound to immutable Java records annotated with `@ConfigurationProperties`.

```java
@ConfigurationProperties(prefix = "app.trading")
public record TradingProperties(
    @NotBlank String brokerUrl,
    @Min(1) int maxOrderQuantity,
    @NotNull Duration executionTimeout
) {}
```

### 2. Profile Management
- `application.yml`: Common default configuration values.
- `application-local.yml`: Development overrides (H2/embedded containers).
- `application-test.yml`: Integration test overrides.
- `application-prod.yml`: Production values (references environment variables).

---

## 3. Spring Security, OAuth2 & JWT Architecture

Spring Security MUST be configured statelessly using `SecurityFilterChain` and functional bean definitions.

### Enterprise Security Filter Chain Template:
```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfiguration {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(Customizer.withDefaults())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health/**", "/v3/api-docs/**", "/swagger-ui/**").permitAll()
                .requestMatchers("/api/v1/public/**").permitAll()
                .requestMatchers("/api/v1/trading/**").hasRole("TRADER")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    }
}
```

---

## 4. Spring Events & Transactional Boundaries

Internal event-driven communication MUST use `@TransactionalEventListener` to enforce that domain events are processed **only after** the publishing transaction successfully commits.

```java
@Component
public class OrderEventListener {

    @Async
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void handleOrderExecuted(OrderExecutedEvent event) {
        // Safe to execute asynchronous side-effects (notifications, audit logging)
    }
}
```

---

## 5. REST Controllers & Bean Validation

1. **Explicit HTTP Verbs & Status Codes**: `GET` (200), `POST` (201 Created), `PUT/PATCH` (200), `DELETE` (204 No Content).
2. **Declarative Bean Validation**: Input request DTOs MUST be annotated with `@Valid` and standard constraints (`@NotNull`, `@NotBlank`, `@Size`, `@Pattern`).
3. **No Entities in Controllers**: REST Controllers MUST accept request DTO records and return response DTO records. JPA Entities MUST NEVER be exposed across HTTP boundaries.
