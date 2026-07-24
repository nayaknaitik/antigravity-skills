# Code Review Skill - User Guide

## Overview
`code-review` acts as a Principal Software Engineer reviewing production pull requests across 15 engineering dimensions. It inherits from `skill-architect`, `production-engineering`, `requirement-analysis`, and `system-architecture`.

## Key Capabilities
- **15 Review Dimensions**: Audits correctness, architecture, security, concurrency, database performance, APIs, observability, testing, maintainability, financial safety, and AI code quality.
- **Severity Classification**: Categorizes findings into `CRITICAL` blockers, `HIGH` issues, `MEDIUM` warnings, and `LOW`/`NIT` suggestions.
- **Automated Verification**: Runs `scripts/code_review_engine.py` to calculate Production Readiness Score (0-100) and risk score.

## How to Trigger Code Review
1. Request a code review on a pull request or code diff.
2. The skill executes automated linting and performs deep architectural audit across all 15 dimensions.
3. Produces structured Markdown Code Review Report.
