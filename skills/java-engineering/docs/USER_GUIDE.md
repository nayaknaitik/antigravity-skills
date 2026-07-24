# Java Engineering Skill - User Guide

## Overview
`java-engineering` provides enterprise-grade Java 21+, Spring Boot 3+, and Spring Modulith engineering capabilities. It inherits standards from `skill-architect`, `production-engineering`, `requirement-analysis`, and `system-architecture`.

## Target Application Types
- Financial & Trading Platforms (OMS, EMS, Portfolio, Risk Management)
- Quantitative Research & Prediction Engines
- AI Inference & RAG Services in Java
- High-Throughput Event-Driven Services (Kafka, RabbitMQ)
- Modular Monoliths & Microservices

## Usage Rules
1. **Java 21 Virtual Threads**: Virtual threads enabled by default (`spring.threads.virtual.enabled=true`).
2. **Modular Monoliths**: Default to Spring Modulith architecture before breaking into microservices.
3. **Immutability**: DTOs and value objects MUST be Java records.
4. **RFC 7807 Error Handling**: Use `@ControllerAdvice` to return `ProblemDetail`.
5. **Observability**: Structured Logback JSON + OpenTelemetry metrics/tracing.
