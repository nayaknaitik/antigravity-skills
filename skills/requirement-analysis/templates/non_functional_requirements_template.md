# Non-Functional Requirements (NFR) Specification Template

## NFR Catalog: {{ SYSTEM_NAME }}

| NFR ID | Category | Target Parameter | Numerical Threshold | Measurement Instrument | Priority |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `NFR-LAT-01` | Latency | Pre-Trade Risk Processing | `< 50 microseconds (p99)` | PTP Hardware Timestamping | MUST |
| `NFR-THR-01` | Throughput | Order Book Aggregation | `> 500,000 msgs/sec` | Synthetic Benchmark Load Generator | MUST |
| `NFR-AVL-01` | Availability | Core Exchange Gateway | `99.999% uptime` | Multi-region Active-Active | MUST |
| `NFR-REL-01` | Reliability | RTO (Recovery Time Objective) | `< 2.0 seconds` | Chaos Engineering Injector | MUST |
| `NFR-SEC-01` | Security | FIX Gateway Auth | `mTLS + TLS 1.3` | Automated Port Scanner | MUST |
