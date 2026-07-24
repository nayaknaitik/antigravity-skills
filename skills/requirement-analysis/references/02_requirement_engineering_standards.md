# Requirement Engineering Standards & Methodology Specification

## 1. Governance & Standards Framework

Our Requirement Analysis methodology synthesizes five international engineering standards:

1. **ISO/IEC/IEEE 29148:2018**: Systems and software engineering — Life cycle processes — Requirements engineering.
2. **IEEE Std 830**: IEEE Recommended Practice for Software Requirements Specifications (SRS).
3. **BABOK v3 (IIBA)**: Business Analysis Body of Knowledge — Domain elicitation and stakeholder analysis.
4. **INCOSE Systems Engineering Handbook**: Requirements verification, traceability, and risk management.
5. **Agile Requirement Engineering & BDD**: User Story Mapping, Event Storming, and Gherkin syntax (`Given-When-Then`).

---

## 2. The Requirement Analysis Spectrum

The requirement-analysis skill evaluates every input across 16 core requirement dimensions:

```
[ Business Idea ] 
       │
       ▼
 1. Business Analysis & Stakeholder Identification
 2. User Journey Mapping & Actor Profiling
 3. Functional Requirement Extraction (FR-XXX)
 4. Non-Functional Requirement Specification (NFR-XXX: Latency, Throughput, Availability)
 5. Business & Domain Rules Extraction (BR-XXX)
 6. Assumptions & Constraints Logging
 7. Risk Analysis & Threat Identification
 8. Edge Case & Failure Mode Scenario Generation
 9. Security & Regulatory Compliance Analysis (SEC-XXX, COMP-XXX)
10. Data & Event Flow Mapping (Kafka, SBE, FIX)
11. API & Database Requirements Specification
12. Observability & Monitoring Requirements (OBS-XXX)
13. Acceptance Criteria Generation (Gherkin Scenarios)
14. Requirement Prioritization (MoSCoW / WSJF)
15. Traceability Matrix Mapping (Goal -> FR -> NFR -> Test Case)
16. Validation & Sign-off Gate
```

---

## 3. Ambiguity Rejection & Clarifying Questionnaire Rules

The `requirement-analysis` skill **STRICTLY REJECTS** vague or ambiguous statements. If an input contains ambiguous terms, the agent MUST pause execution and ask targeted clarifying questions.

### 3.1 Ambiguity Detection Matrix

| Ambiguous Word / Phrase | Why It Is Rejected | Required Measurable Metric |
| :--- | :--- | :--- |
| *"Fast" / "Real-time"* | Unquantifiable latency target | Latency in milliseconds or microseconds at p99 / p99.9 (e.g. `< 500μs at p99`). |
| *"Scalable"* | Vague capacity bound | Throughput in messages/sec or orders/sec (e.g. `100,000 msg/sec per node`). |
| *"High availability"* | Vague uptime target | System uptime SLA percentage (e.g. `99.999% uptime`, max 5.26 min downtime/yr). |
| *"Secure"* | Vague security posture | Encryption standard, authentication protocol, regulatory standard (e.g. `AES-256`, `OAuth2/OIDC`, `SOC2 Type II`). |
| *"User-friendly"* | Subjective UI/UX statement | Max click count, page load time, task completion rate (e.g. `< 3 clicks to place order`, `< 100ms UI render`). |
| *"Robust / Fault-tolerant"* | Vague resilience statement | Recovery Time Objective (RTO) and Recovery Point Objective (RPO) (e.g. `RTO < 5s`, `RPO = 0`). |

---

## 4. Behavior Driven Development (BDD) & Gherkin Syntax

Every functional requirement MUST be accompanied by executable BDD Acceptance Criteria using Gherkin syntax:

```gherkin
Feature: Order Risk Limit Validation
  As a Quantitative Trader
  I want my orders validated against pre-trade risk limits
  So that abnormal orders do not breach capital thresholds.

  Scenario: Order exceeds maximum order value threshold
    Given a trader account with a maximum order limit of $500,000 USD
    And the market price of AAPL is $150 USD
    When the trader submits a BUY order for 5,000 shares of AAPL ($750,000 USD total)
    Then the Risk Engine MUST REJECT the order within 250 microseconds
    And an order rejection notification MUST be emitted with error code "RISK_EXCEEDS_MAX_ORDER_VALUE"
    And the order status MUST be updated to "REJECTED".
```
