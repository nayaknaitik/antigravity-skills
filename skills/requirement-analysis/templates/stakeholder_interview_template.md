# Stakeholder Interview Elicitation Template

## 1. Interview Metadata
- **Interviewee Name**: {{ INTERVIEWEE_NAME }}
- **Role / Department**: {{ ROLE_DEPARTMENT }} (e.g. Head of Quant Trading / Chief Risk Officer)
- **Interviewer**: {{ INTERVIEWER_NAME }}
- **Date & Time**: {{ INTERVIEW_DATE }}

---

## 2. Core Elicitation Questions

### 2.1 Business Objectives & Value Drivers
- What core problem or trading opportunity does this feature address?
- How do we measure success for this initiative? (Specific revenue, Sharpe ratio, or latency reduction target)

### 2.2 Operational & Functional Boundaries
- Who are the direct human users and automated software actors interacting with this feature?
- What are the mandatory business rules and exchange regulatory compliance boundaries?

### 2.3 Non-Functional Bounds & Stress Conditions
- What is the maximum acceptable latency for this operation?
- What happens if market data volume spikes 10x during an unexpected news event?
- What is the acceptable Recovery Point Objective (RPO) if a server node crashes?

---

## 3. Clarifications & Disambiguation Log
| Ambiguous Statement | Clarified Quantitative Metric | Final Requirement Link |
| :--- | :--- | :--- |
| *"Needs to be fast"* | Latency must be `< 100 microseconds` | `NFR-LAT-01` |
