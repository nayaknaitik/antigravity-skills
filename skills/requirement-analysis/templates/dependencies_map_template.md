# Dependency Analysis Map Template

## System Dependencies: {{ SYSTEM_NAME }}

| Dependency ID | Upstream / Downstream Component | Interface Protocol | Data Contract | Criticality |
| :--- | :--- | :--- | :--- | :---: |
| `DEP-01` | Market Data Feed Handler | SBE over UDP Multicast | Normalized `TickBar` stream | CRITICAL |
| `DEP-02` | Pre-Trade Risk Engine | Shared Memory IPC | `OrderRiskCheckResult` struct | CRITICAL |
