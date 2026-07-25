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

## 2. Mode A: Continuous Monitoring Loop

When invoked as a continuous monitor, execute this state machine:

1. **Define Baseline**: Pull the trailing 24h average for target metrics (latency, error rate, saturation).
2. **Run Checks**: Execute checks across all observability layers (Availability, Errors, Latency, Saturation, Dependency, Correctness, Change Correlation).
3. **Compare**: Check current metrics against baseline using `references/check_thresholds.md`.
4. **Classify**: Assign severity (CRITICAL, WARNING, INFO).
   - *INFO* -> Log only.
   - *WARNING* -> Flag in summary report.
   - *CRITICAL* -> Fire alert and **Hard Transition to Mode B**.

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

## 6. Report Template

Upon closing an investigation, fill and output this template. **Every section below is mandatory — do not omit a section because it's empty; state "None found" explicitly instead.** This report is the audit trail a human will trust in place of redoing the investigation themselves, so incompleteness here is a safety gap, not a style issue.

```markdown
## Observability & Debug Incident Report

**Summary**: [1-sentence description of the issue and final state]
**Timeline**: 
- [Use the actual current/event timestamp, e.g. 2026-07-24T10:02:00Z — never a placeholder like "[Current Time]"]
- [HH:MM] Alert triggered / Investigation started
- [HH:MM] Hypothesis confirmed
- [HH:MM] Action taken / Escalated

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

### Budget & Rate Limit Check
- Automated remediation attempts for this service in the last hour: [N/3]
- Query iterations used this investigation: [N/10]
- [If either cap is at or near limit, this must force ESCALATE regardless of confidence — state that explicitly here]

### Action Taken
- **Decision**: [Escalated to human | Auto-Fix executed]
- **Details**: [Describe the rollback, restart, or escalation target. If escalation was skipped because the action is allowlisted, say "Escalation not required — matches pre-approved allowlist entry [issue-type/action pair]," never "bypassed."]
- **Rollback Plan**: [If action was taken, how to revert it]
- **Monitoring Window**: [Duration per the Section 5 table, and current status: in-progress / passed / recurred]

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
