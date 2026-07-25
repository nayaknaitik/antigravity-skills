# Check Categories & Thresholds

When operating in Mode A (Continuous Monitoring) or collecting context in Mode B, evaluate metrics against this explicit tiering matrix. If a check crosses a CRITICAL threshold, immediately transition to Mode B (Debug).

| Check Category | Metric / Sub-Check | INFO | WARNING | CRITICAL | Default Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Availability** | HTTP Status / Health Endpoint | 200 OK | >1 missed ping in 5m | Down for >60s | CRITICAL -> Alert & Debug |
| **Errors** | 5xx Rate vs Baseline | < 1% above baseline | > 2% above baseline | > 5% above baseline | CRITICAL -> Alert & Debug |
| **Errors** | New Log Signatures | Seen before | 1 new error signature | >3 new unique signatures | WARNING -> Flag in report |
| **Latency** | p95 Response Time | <= Baseline | Baseline + 20% | Baseline + 50% | CRITICAL -> Alert & Debug |
| **Latency** | LCP (Web Vitals) | <= 2.5s | 2.5s - 4.0s | > 4.0s | WARNING -> Flag in report |
| **Saturation** | CPU Utilization | < 70% | 70% - 85% | > 85% for 5m | CRITICAL -> Alert & Debug |
| **Saturation** | Connection Pool | < 60% used | > 80% used | > 95% used | CRITICAL -> Alert & Debug |
| **Dependencies** | Upstream API Status | 200 OK | Elevated latency (>50%) | 5xx or Timeout | CRITICAL -> Alert & Debug |
| **Correctness** | DOM/Payload structure | Valid JSON/HTML | Missing non-critical fields| Missing critical body data| CRITICAL -> Alert & Debug |
| **Change Correlation**| Deploys / Feature Flags | None in 24h | Change in last 4h | Change in last 30 mins | N/A (Used as context multiplier) |
