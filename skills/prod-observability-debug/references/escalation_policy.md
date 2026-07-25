# Escalation Policy

If the skill decides to **ESCALATE** via the Decision Gate, or if an automated remediation fails the closed-loop verification, it must strictly follow this policy.

## Escalation Targets
1. **Primary**: PagerDuty/OpsGenie webhook for the on-call engineer associated with the failing service.
2. **Secondary**: Dedicated `#incident-triage` Slack or Teams channel.

## Escalation Packet Format
When escalating, the skill MUST deliver an Escalation Packet containing:
- **Severity**: The assigned tier (CRITICAL / WARNING).
- **Symptom**: 1-sentence description of the breached threshold.
- **Top Hypothesis**: The highest confidence hypothesis generated in Mode B.
- **Links**: Direct URLs to the relevant APM trace, log query, or metrics dashboard to save the human responder time.

## Timeout & Fallback Behavior
- If an automated query or trace retrieval takes longer than `60 seconds`, the skill should timeout that specific query, mark confidence as `Low`, and escalate.
- If the primary escalation target (PagerDuty API) is down, the skill must fallback to posting the Escalation Packet in the secondary Slack channel and tagging `@here`.
