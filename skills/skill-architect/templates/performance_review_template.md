# Performance & Efficiency Audit Specification

## Target System: {{ SYSTEM_NAME }}

### 1. Token & Context Optimization
- [ ] Large reference manuals lazy-loaded from `references/` rather than inline in `SKILL.md`
- [ ] No redundant context duplication in system prompts

### 2. Execution Benchmarks
| Benchmark Metric | Threshold | Measured Value | Status |
| :--- | :--- | :--- | :---: |
| Validator Execution Time | < 1.0s | 0.25s | PASS |
| Quality Scorer Time | < 2.0s | 0.45s | PASS |
| Memory Consumption | < 100MB | 32MB | PASS |
