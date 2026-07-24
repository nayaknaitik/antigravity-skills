# Requirement Verification Checklists, Matrices & Protocols

## 1. Requirement Quality Verification Checklist

Before a requirement document is approved for baseline, it MUST satisfy all 8 quality dimensions:

- [ ] **1. Completeness**: Does every requirement specify inputs, outputs, preconditions, postconditions, and error paths?
- [ ] **2. Unambiguity**: Are all vague terms replaced with concrete numerical bounds?
- [ ] **3. Testability**: Can a QA or Automated Test Engineer write an automated pass/fail test for this requirement?
- [ ] **4. Consistency**: Are there zero conflicting business rules or contradictory latency targets?
- [ ] **5. Feasibility**: Is the latency or throughput target achievable within current hardware/network constraints?
- [ ] **6. Traceability**: Is every Functional Requirement linked to a parent Business Goal and child Test Case?
- [ ] **7. Security & Compliance**: Are pre-trade risk controls and regulatory audit rules explicitly stated?
- [ ] **8. BDD Coverage**: Does every functional requirement include at least one Gherkin `Given-When-Then` scenario?

---

## 2. Quantitative Trading Risk & Edge Case Checklist

Evaluate every feature against trading edge cases:

1. **Market Data Anomalies**:
   - Order book crossed or locked (Bid > Ask).
   - Stale market data feeds (> 500ms since last tick).
   - Packet loss / gap in sequence numbers.
   - Out-of-order tick arrival.
2. **Execution & Exchange Anomalies**:
   - Exchange gateway disconnect during order inflight state.
   - Partial fills followed by immediate exchange cancellation.
   - Order rejected due to exchange circuit breaker activation.
   - Self-trade prevention (STP) trigger by internal desk accounts.
3. **System Risk Anomalies**:
   - Market volatility spike causing 10x normal order volume.
   - Memory exhaustion or disk space write error on trade journaler.
   - Primary broker connection drop; failover to secondary broker.

---

## 3. Requirement Traceability Matrix Schema

Every project baseline requires a complete Traceability Matrix mapping:

```
[ Business Goal BG-01 ] ──► [ Functional Req FR-01 ] ──► [ System Spec OMS-101 ] ──► [ Test Case TC-OMS-101 ]
                        └──► [ Non-Functional NFR-01 ] ──► [ Performance Test PT-01 ]
```
