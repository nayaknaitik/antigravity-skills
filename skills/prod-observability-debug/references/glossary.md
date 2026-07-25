# Observability Glossary

- **APM (Application Performance Monitoring)**: Tools used to track application performance, tracing, and code-level bottlenecks (e.g., Datadog, New Relic).
- **Baseline**: The normal, average operating state of a metric over a defined historical window (e.g., trailing 24 hours), used for comparison against current anomalies.
- **Blast Radius**: The scope of impact a failure or a remediation action has on the system. A "High" blast radius impacts all users; "Low" impacts a tiny subset or a background worker.
- **CLS (Cumulative Layout Shift)**: A Core Web Vital measuring visual stability of a webpage.
- **Correlation vs. Causation**: Correlation means two events happened at the same time (e.g. "a deploy happened and errors spiked"). Causation means one event directly triggered the other, proven by evidence (e.g. "the deploy introduced a missing variable causing the exact error stack trace").
- **INP (Interaction to Next Paint)**: A Core Web Vital assessing a page's overall responsiveness to user interactions.
- **LCP (Largest Contentful Paint)**: A Core Web Vital measuring the load time of the main page content.
- **p50 / p95 / p99**: Percentiles for latency. p95 means 95% of requests are completed in this time or faster. It helps ignore extreme outliers while tracking realistic worst-case performance.
- **SLA (Service Level Agreement)**: A formal commitment to uptime and performance standards (e.g., 99.9% uptime).
- **Web Vitals**: A set of standardized metrics created by Google to measure user experience on the web (includes LCP, CLS, INP).
