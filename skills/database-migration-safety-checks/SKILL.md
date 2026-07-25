---
name: database-migration-safety-checks
description: Assesses database migration scripts for locking, downtime, and destructive risks before execution. Triggered when a PR modifying SQL schemas is opened, or when explicitly invoked with a migration file path.
---

# Database Migration Safety Checks

This skill evaluates incoming database migration scripts to prevent production downtime, data loss, or table locks. 

## 1. Trigger Conditions
- **Automated**: A PR is opened or updated containing files matching `**/*migration*.sql` or `**/*V*__*.sql`.
- **Manual**: Explicit invocation by a user via `Verify this migration: [file_path]`.

## 2. Guardrails (Non-Negotiable)
- **Least Privilege**: The skill operates in **READ-ONLY** mode. It may read schema states, read migration scripts, and post PR comments. It MUST NEVER apply migrations or execute DDL/DML in any environment.
- **Denylist**: Never approve migrations containing `DROP TABLE`, `DROP DATABASE`, or `TRUNCATE` autonomously.
- **Allowlist**: Autonomous approval is ONLY allowed for non-blocking index additions (e.g., `CREATE INDEX CONCURRENTLY`), simple row inserts (e.g., `< 1000 rows`), or safe column additions (`ADD COLUMN` without a volatile default).
- **Audit Trail**: Every decision is logged as a structured JSON summary output.

## 3. Workflow State Machine

### Phase 1: Detect & Gather Context
- **Entry**: Migration file path is provided.
- **Action**: Parse the SQL script and identify the target database. Extract current table sizes and existing indexes using `references/schema-queries.md`.
- **Exit**: A parsed AST/list of operations and current table metadata.

### Phase 2: Diagnose & Categorize (HARD GATE)
- **Entry**: Parsed operations available.
- **Action**: Evaluate each operation against the Decision Table below.
- **Exit**: Categorization of the migration as `SAFE`, `WARNING`, or `CRITICAL`.

### Phase 3: Decide & Recommend
- **Entry**: Migration categorized.
- **Action**: Formulate recommendations. If `CRITICAL`, prepare escalation protocols. If `WARNING`, prepare mitigation steps (e.g., batching).
- **Exit**: Drafted decision report.

### Phase 4: Verify & Report
- **Entry**: Drafted report ready.
- **Action**: Output the final structured report using the template from `references/output-template.md`.
- **Exit**: Report delivered to the user or PR.

## 4. Decision Table (Risk Thresholds)

Evaluate the migration script line-by-line using this table. When evidence is ambiguous, default to the **CRITICAL** tier.

| Operation / Condition | Threshold | Tier | Required Action / Mitigation |
| :--- | :--- | :--- | :--- |
| `ADD COLUMN` | With `DEFAULT` value (not null) on table > 100k rows | **CRITICAL** | Escalate. Rewrite as: add col -> backfill -> set default. |
| `ADD COLUMN` | No `DEFAULT` / table < 100k rows | **SAFE** | Approve automatically. |
| `CREATE INDEX` | Without `CONCURRENTLY` on table > 10k rows | **CRITICAL** | Escalate. Require `CREATE INDEX CONCURRENTLY`. |
| `CREATE INDEX` | With `CONCURRENTLY` | **SAFE** | Approve automatically. |
| `DROP COLUMN` / `RENAME` | Any | **WARNING** | Flag for human review to ensure app-side backwards compatibility. |
| `DROP TABLE` / `TRUNCATE` | Any | **CRITICAL** | Escalate. Denied by default. |
| `UPDATE` / `DELETE` | Missing `WHERE` clause OR rows > 10k | **CRITICAL** | Escalate. Require batching (e.g., chunks of 1k). |

## 5. Verification & Closed-Loop Checks
- **Monitoring Window**: If the migration is run by a human, recommend monitoring DB CPU and Active Connections for 15 minutes post-deployment.
- **Baseline Comparison**: Compare execution times of similar historical queries against the stored baseline.
- **Failure Protocol**: If verification fails or execution times out, instruct the user to immediately trigger procedures from `references/rollback-procedures.md`.

## 6. References & External Modules
- [Glossary & Terms](references/glossary.md)
- [Rollback Procedures](references/rollback-procedures.md)
- [Output Template](references/output-template.md)
- [Rollout Checklist](references/rollout_checklist.md)
