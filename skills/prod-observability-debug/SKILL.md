---
name: prod-observability-debug
description: Unified skill for continuous system health monitoring and reactive production issue debugging. Triggered proactively ("monitor this service," "watch after deploy," "check system health") or reactively ("something's broken," "investigate this error," "debug this alert").
---

# Production Observability & Debug

This skill enables the agent to continuously monitor system health (Mode A) and seamlessly transition into deep diagnostic debugging and remediation (Mode B) when thresholds are crossed or when explicitly invoked.

## 1. Guardrails (Non-Negotiable)

- **Least Privilege (Read/Write)**: The skill operates globally in **READ-ONLY** mode by default (logs, metrics, traces, git history). Remediation (write access) is blocked unless the action precisely matches the **Allowlist**.
- **Denylist (Never Automate)**: Data deletion, schema changes, credential/IAM modifications, and billing-affecting operations.
- **Allowlist**: Autonomous fixes are ONLY permitted for pre-approved action pairs: e.g. `[Issue: Memory Leak / Action: Restart Container]`, `[Issue: Bad Deploy / Action: Trigger Rollback Skill]`.
- **Budgets & Rate Limits**: Maximum of 3 automated remediation attempts per hour per service. Maximum 10 query iterations per investigation phase. Exceeding limits forces immediate escalation.
- **Kill Switch**: If `[ABORT_AUTONOMY]` is passed in the prompt or monitoring config, the skill drops to Read-Only reporting mode instantly.
- **Audit Trail**: Every check, baseline comparison, hypothesis formed, and action taken MUST be documented in the final report.
- **Evidence Integrity (Non-Negotiable)**: Every factual claim in any report must trace to something actually present in the ingested alert, logs, or metrics.
  - If a value (severity, owner, SLA, dependency status, etc.) was not explicitly provided in the input, the skill MUST NOT state that it was "explicitly defined," "specified," or "confirmed via" the source.
  - Where a value is inferred rather than sourced, state plainly: `"[field] not provided in input — inferred as [X] based on [reasoning]."`
  - Fabricating a source for an inferred value is treated as a **critical failure** of this skill, equivalent in severity to an unauthorized remediation action, and must be self-reported as such if discovered after the fact.

## 2. Mode A: Continuous Monitoring Loop

When invoked as a continuous monitor, execute this state machine:

1. **Define Baseline**: Pull the trailing 24h average for target metrics (latency, error rate, saturation).
2. **Run Checks**: Execute checks across all observability layers (Availability, Errors, Latency, Saturation, Dependency, Correctness, Change Correlation).
3. **Compare**: Check current metrics against baseline using `references/check_thresholds.md`.
4. **Classify**: Assign severity (CRITICAL, WARNING, INFO).
   - *INFO* -> Log only.
   - *WARNING* -> Flag in summary report.
   - *CRITICAL* -> Fire alert and **Hard Transition to Mode B**.

### 2.5 Severity Mapping (Deviation Tier → Incident Priority)

CRITICAL/WARNING/INFO describe metric deviation, not business-facing incident priority (P1–P4). These are not the same axis and must not be conflated.

- If the ingested alert payload explicitly carries a P1–P4 (or equivalent) priority field, use it verbatim and cite the exact field/value in the report.
- If no such field is present, derive one — do not leave it unstated and do not assume a source that isn't there:
  - CRITICAL tier + user-facing revenue/critical path + no viable fallback or load-balanced degradation → **P1**
  - CRITICAL tier + partial degradation (traffic still substantially succeeding, load-balanced, isolated service) → **P2**
  - WARNING tier, any path → **P3**
  - INFO tier → **P4**
- In every report, state explicitly whether the priority was **(a) sourced** from the payload (quote the field) or **(b) derived** here (show the reasoning). Never present a derived value as if it were sourced — this is covered by the Evidence Integrity guardrail in Section 1.

## 3. Mode B: Reactive Debug & Remediation

When transitioning from Mode A (CRITICAL alert) or when invoked explicitly by a human (e.g. "investigate 5xx spike"):

1. **Ingest Signal**: Parse the incoming alert payload, Slack message, or failing health check.
2. **Gather Context**: Query logs, APM traces, and metrics. Cross-reference against recent deployment hashes and feature-flag changes in the last 1-4 hours.
3. **Diagnose**: Formulate a list of **Ranked Hypotheses**. Every hypothesis must include:
   - Supporting evidence (specific log IDs, metric charts).
   - Confidence score (High, Medium, Low).
   - State of confirmation (Correlated vs. Causation Confirmed).
4. **Decide (HARD GATE)**: Evaluate the top hypothesis against the **Fix vs. Escalate Table** below.
5. **Act/Escalate**: Execute the approved action or trigger the escalation protocol.
6. **Verify**: Perform closed-loop verification (see section 5).
7. **Record**: Generate the final Incident Report.

## 4. Decision Gate: Fix vs. Escalate

If the leading hypothesis points to a fix, evaluate it here. **Default to Escalate if ambiguous.**

| Environment | Action Reversibility | Confidence Level | Blast Radius | On Allowlist | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Prod | Irreversible | Any | Any | Any | **ESCALATE** |
| Prod | Reversible | Low/Medium | High/Global | Any | **ESCALATE** |
| Prod | Reversible | High | Low/Isolated | No | **ESCALATE** |
| Prod | Reversible | High | Low/Isolated | Yes | **AUTO-FIX** |
| Non-Prod | Reversible | Medium/High | Any | Yes | **AUTO-FIX** |

When a decision is made, the report must show the match against **all five columns explicitly** (Environment, Reversibility, Confidence, Blast Radius, Allowlist status) — not merely assert that a row was matched.

## 5. Closed-Loop Verification

A remediation is NEVER "fire and forget".
1. **Multi-Signal Success**: Resolution requires the original alerting metric returning to baseline AND an independent health check (e.g., synthetic endpoint test) passing.
2. **Baseline Comparison**: The post-fix state must be compared against the stored pre-incident baseline, not absolute hardcoded values.
3. **Monitoring Window**: The skill must pause and observe metrics post-fix for a duration set by severity and environment — do not invent a duration ad hoc:

   | Severity | Environment | Monitoring Window |
   | :--- | :--- | :--- |
   | P1 | Prod | 30 minutes |
   | P2 | Prod | 20 minutes |
   | P1/P2 | Non-Prod | 10 minutes |
   | P3/P4 | Any | 5 minutes |

4. **Failure Protocol**: If verification fails or the incident recurs within the window, the skill MUST escalate to a human. Silent re-attempts with unapproved fixes are forbidden.

### 5.1 Independent Signal Requirement

The independent check must be something other than the original alerting metric — e.g. a synthetic transaction, a separate health endpoint probe, or a canary request. Restating the same metric that triggered the alert does not satisfy this requirement.

- If an independent-check tool/mechanism is available in this environment, run it and report its result explicitly.
- If no independent-check mechanism is available, verification is **INCOMPLETE**, not passed. The report must state: `"Independent signal unavailable — verification based on primary metric only. Recommend manual confirmation."`
- Under this condition, do not mark the incident status as `RESOLVED`. Mark it `RESOLVED (metric-only, unconfirmed)` and surface it for human confirmation.

## 6. Report Template

Upon closing an investigation, fill and output this template. **Every section below is mandatory — do not omit a section because it's empty; state "None found" explicitly instead.** This report is the audit trail a human will trust in place of redoing the investigation themselves, so incompleteness here is a safety gap, not a style issue.

```markdown
## Observability & Debug Incident Report

**Summary**: [1-sentence description of the issue and final state]
**Severity**: [P1-P4] — [Source: quoted field from payload, OR "not provided in input — derived per Section 2.5, see reasoning below"]
**Timeline**: 
- [Use the actual current/event timestamp, e.g. 2026-07-24T10:02:00Z — never a placeholder like "[Current Time]"]
- [HH:MM] Alert triggered / Investigation started
- [HH:MM] Hypothesis confirmed
- [HH:MM] Action taken / Escalated  [label must match the actual decision made — do not leave template wording unedited]

### Check Results
List every check category actually run against `references/check_thresholds.md`, not only the one(s) that fired. Checks that came back clean or couldn't be run are still required rows.

| Check Category | Metric Result | Baseline | Deviation / Tier |
| :--- | :--- | :--- | :--- |
| [e.g. Errors] | [e.g. 9.1%] | [e.g. 0.4%] | [CRITICAL] |
| [e.g. Latency] | [e.g. 210ms] | [e.g. 200ms] | [OK] |
| [e.g. Recent Changes] | [e.g. canary deploy, 8 min ago] | [e.g. none pre-incident] | [RULED IN / RULED OUT] |
| [e.g. Dependency Health] | [result, or "not checked — data source unavailable"] | | |

### Ranked Hypotheses
1. **[Hypothesis 1]** - Confidence: [High/Med/Low] - Status: [Confirmed/Correlated]
   - *Evidence*: [Link to logs/traces/deploy PR]
2. **[Hypothesis 2]**...

### Severity Justification
- [Why P1/P2/P3/P4 was chosen if not explicitly defined upstream]

### Decision Gate Evaluation
- Environment: [Prod/Non-Prod]
- Action Reversibility: [Reversible/Irreversible]
- Confidence Level: [High/Med/Low]
- Blast Radius: [High/Low]
- Allowlist Match: [Yes/No]

### Budget & Rate Limit Check
- Automated remediation attempts for this service in the last hour: [N/3]
- Query iterations used this investigation: [N/10]
- [If either cap is at or near limit, this must force ESCALATE regardless of confidence — state that explicitly here]

### Action Taken
- **Decision**: [Escalated to human | Auto-Fix executed]
- **Details**: [Describe the rollback, restart, or escalation target. If escalation was skipped because the action is allowlisted, say "Escalation not required — matches pre-approved allowlist entry [issue-type/action pair]," never "bypassed."]
- **Rollback Plan**: [If action was taken, how to revert it]
- **Monitoring Window**: [Duration per the Section 5 table, based on the Severity stated above — and current status: in-progress / passed / recurred]
- **Independent Signal Check**: [Required per Section 5.1. Name the specific check run and its result, OR state explicitly that no independent-check mechanism was available and that resolution is metric-only/unconfirmed.]

### If Escalated — Escalation Packet
- **Suggested next step for the human**: [the top hypothesis's fix, even if the agent isn't allowed to execute it itself — never leave the human with nothing to start on]
- **Evidence summary**: [2-3 lines, not the full log dump]
- **Escalation channel status**: [confirm whether the page/webhook actually fired and whether it was acknowledged — don't just state intent]
- **Full record link**: [link back to this report / raw logs examined]
```

## 7. Integration Points
- **Alert Ingestion**: PromQL, Datadog API, AWS CloudWatch, PagerDuty webhooks.
- **Upstream Triggers**: CI/CD deployment pipelines (invoking Mode A for post-deploy checks).
- **Downstream Actions**: Handoffs to `deployment-rollback` skill or Github Actions.

## 8. References
- [Check Thresholds](references/check_thresholds.md)
- [Glossary](references/glossary.md)
- [Escalation Policy](references/escalation_policy.md)
- [Rollout Checklist](references/rollout_checklist.md)