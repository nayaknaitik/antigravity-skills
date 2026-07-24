# Production Engineering Skill - Inheritance Guide

## How Language Skills Inherit `production-engineering`

`production-engineering` is the root skill inherited by every language-specific skill:
- `rust-engineering`
- `go-engineering`
- `java-engineering`
- `typescript-engineering`
- `python-engineering`

### The Inheritance Contract
Every language-specific skill MUST:
1. Reference `production-engineering` in its activation rules and purpose section.
2. Translate root principles into language-native idioms:
   - **Timeouts & Cancellation**: Go `context.Context` / Rust `tokio::time::timeout` / Java `CompletableFuture.orTimeout`.
   - **Dependency Injection**: Go manual wire-up / Rust trait object injection / Java Spring/Guice DI.
   - **Error Handling**: Go `error` returns / Rust `Result<T, E>` / Java typed exception hierarchies.
   - **Observability**: OpenTelemetry SDK bindings for the target language.
3. Validate that generated code complies with `production_readiness_checker.py`.
