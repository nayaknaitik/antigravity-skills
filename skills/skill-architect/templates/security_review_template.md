# Security Review & Threat Audit Specification

## Target System: {{ SYSTEM_NAME }}

### 1. Credentials & Secrets Check
- [ ] ZERO API keys, tokens, SSH keys, or passwords committed
- [ ] Environment variables used for all sensitive configuration

### 2. Path Traversal & Injection Prevention
- [ ] User-supplied paths sanitized and resolved (`Path.resolve()`)
- [ ] Shell executions use array args, avoiding raw string interpolation

### 3. Data Protection & Privacy (PII)
- [ ] No customer PII stored in test fixtures or logs
- [ ] Log outputs stripped of sensitive token data
