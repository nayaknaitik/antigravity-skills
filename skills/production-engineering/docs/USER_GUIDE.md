# Production Engineering Skill - User Guide

## Overview
`production-engineering` is the root architectural engineering skill of our organization. It provides language-agnostic standards, templates, scripts, and validation rules for building production-ready software.

## How to Apply this Skill
When generating software or auditing architectures:
1. **Inheritance**: Language-specific skills (e.g. `rust-engineering`, `go-engineering`, `java-engineering`, `typescript-engineering`) inherit all principles from `production-engineering`.
2. **Architecture Blueprinting**: Use `templates/01_production_service_blueprint.yaml.template` to define your target service.
3. **Automated Verification**: Run `python3 scripts/production_readiness_checker.py --spec <your_blueprint.yaml>` to verify compliance before writing code.
4. **Resilience & Telemetry**: Enforce timeouts, full-jitter retries, circuit breakers, and OpenTelemetry logging/tracing across all generated endpoints.
