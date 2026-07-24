# Spring Boot 3+ Enterprise Development Guide

## Key Standards
1. **Virtual Threads**: Enable via `spring.threads.virtual.enabled=true`.
2. **Spring Modulith**: Encapsulate features in top-level package modules.
3. **Problem Details**: Use Spring 6 `ProblemDetail` in `@RestControllerAdvice`.
4. **Security**: Stateless JWT / OAuth2 resource server via `SecurityFilterChain` bean.
5. **Micrometer & OTel**: Actuator endpoints with Prometheus metric exposition.
