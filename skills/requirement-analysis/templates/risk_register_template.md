# Requirement Risk Register Template

## Risk Register: {{ SYSTEM_NAME }}

| Risk ID | Hazard Description | Probability | Severity | Risk Score | Mitigation Strategy | Owner |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `RSK-01` | Market data burst causes buffer overflow | LOW | HIGH | HIGH | Ring buffer with lock-free backpressure | Lead Quant Dev |
| `RSK-02` | Stale market data leads to wrong execution | MED | HIGH | CRITICAL | Pre-trade tick staleness check (`< 500ms`) | Risk Manager |
