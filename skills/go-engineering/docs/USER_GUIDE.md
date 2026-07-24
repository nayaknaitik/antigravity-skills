# Go Engineering Skill - User Guide

## Overview
`go-engineering` provides cloud-native, high-performance, resilient, observable, and idiomatic Go engineering standards. It inherits from `skill-architect`, `production-engineering`, `requirement-analysis`, and `system-architecture`.

## Key Principles
1. **Idiomatic Go**: "Accept interfaces, return structs", small interfaces, explicit dependencies.
2. **Goroutine Safety**: Every goroutine MUST be bound to a `context.Context` cancellation or channel drain signal.
3. **Structured Logging**: Use standard library `log/slog` for single-line JSON logging.
4. **Error Handling**: Wrap errors with context (`fmt.Errorf("... %w", err)`), inspect with `errors.Is`/`errors.As`. Never panic in production handlers.
5. **Standard Project Layout**: `cmd/`, `internal/`, `pkg/`, `db/migrations/`.
