# Project Assumptions Log Template

## System: {{ SYSTEM_NAME }}

| Assumption ID | Statement of Assumption | Rationale / Source | Risk if Invalidated | Validation Status |
| :--- | :--- | :--- | :--- | :---: |
| `ASM-01` | Exchange market data feeds deliver PTP nanosecond timestamps. | CME FIX Specification | High latency drift in backtest | Verified |
| `ASM-02` | Hardware network interface cards (NIC) support Solarflare EF_VI API. | Infrastructure Team | Sub-optimal kernel bypass | Pending |
