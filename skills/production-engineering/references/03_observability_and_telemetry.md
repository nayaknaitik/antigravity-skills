# 03. Observability, Telemetry & OpenTelemetry Standards

This reference specifies organization-wide standards for logging, metrics, distributed tracing, and OpenTelemetry (OTel) instrumentation based on CNCF best practices.

---

## 1. The Three Pillars of Observability

Observability requires structured, correlated data across three distinct signals:

```
          +----------------------------------------------------+
          |              UNIFIED OBSERVABILITY                 |
          +----------------------------------------------------+
          |  Structured Logs  |  Metrics (RED/USE) |  Traces   |
          +----------------------------------------------------+
          |                   Trace Context                    |
          |       (trace_id, span_id, parent_span_id)          |
          +----------------------------------------------------+
```

---

## 2. Structured JSON Logging Contract

Plain text logs are prohibited in production. All logs MUST be output to `stdout`/`stderr` as single-line JSON objects conforming to the standard schema:

### Standard Log Field Schema:
```json
{
  "timestamp": "2026-07-23T14:30:00.123456Z",
  "level": "INFO",
  "service": "payment-service",
  "version": "1.4.2",
  "environment": "production",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "message": "Payment processed successfully",
  "context": {
    "user_id": "usr_99812",
    "order_id": "ord_5514A",
    "amount": 49.99,
    "currency": "USD",
    "payment_gateway": "stripe"
  },
  "error": {
    "kind": "None"
  }
}
```

### Log Levels & Rules:
- **FATAL / CRITICAL**: System unusable, immediate process crash.
- **ERROR**: Operation failed, unhandled exception, data loss risk, requires engineer intervention.
- **WARN**: Degraded operation, transient failure recovered by retry, fallback activated.
- **INFO**: Key state transitions, milestone business events (e.g., `OrderPlaced`, `UserRegistered`).
- **DEBUG**: Low-level operational detail for troubleshooting (disabled in production by default).

### Anti-Patterns:
- *Prohibited*: Logging sensitive PII (credit cards, passwords, tokens, SSNs).
- *Prohibited*: Log spamming inside hot loops.
- *Prohibited*: Unstructured multi-line stack traces (format stack traces as JSON strings under `error.stack_trace`).

---

## 3. Distributed Tracing & W3C TraceContext

Services MUST propagate W3C `traceparent` headers (`00-{trace_id}-{span_id}-{trace_flags}`) across HTTP, gRPC, and message queues.

### Trace Instrumentation Standards:
1. **Root Span**: Gateway/Entry points create the root span.
2. **Span Propagation**: Downstream RPC or HTTP calls pass current trace context via headers.
3. **Database & External Spans**: Automatically trace database queries, cache lookups, and outbound HTTP requests.
4. **Span Attributes**: Attach standard semantic conventions (`http.status_code`, `db.system`, `rpc.method`).

---

## 4. Metrics Standards (RED & USE Frameworks)

Every service MUST expose a `/metrics` endpoint in Prometheus text format or push OTLP metrics.

### 1. RED Method (For Request-Driven Services):
- **Rate**: Request throughput count per second (e.g., `http_requests_total{status="200"}`).
- **Errors**: Failed request count per second (e.g., `http_requests_total{status=~"5.."}`).
- **Duration**: Request latency histogram distribution (e.g., `http_request_duration_seconds_bucket`).

### 2. USE Method (For Infrastructure & Backing Services):
- **Utilization**: Percentage of time resource is busy (e.g., `cpu_utilization_ratio`, `db_connection_pool_active`).
- **Saturation**: Amount of extra work queued (e.g., `thread_pool_queue_depth`, `disk_io_wait_seconds`).
- **Errors**: Resource error count (e.g., `db_connection_timeouts_total`).

### Metric Naming Conventions:
- Standard units: `_seconds`, `_bytes`, `_total`.
- Format: `<namespace>_<subsystem>_<name>_<unit>`.

---

## 5. OpenTelemetry Collector & Exporters

Services MUST configure the OpenTelemetry SDK with OTLP exporters (`OTLP/gRPC` or `OTLP/HTTP`) pointing to local sidecars or central collectors.

### Default Environment Variables:
```env
OTEL_SERVICE_NAME=payment-service
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.observability.svc.cluster.local:4317
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
```
