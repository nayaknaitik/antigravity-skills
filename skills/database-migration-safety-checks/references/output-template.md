# Migration Assessment Report Template

Use the following markdown template when generating the final assessment report for a PR or user.

```markdown
## Database Migration Safety Assessment

**Status**: [ SAFE | WARNING | CRITICAL ]
**File**: `[migration_file_name.sql]`

### 1. Operations Breakdown
| Operation | Target Table | Estimated Row Count | Risk Tier |
| :--- | :--- | :--- | :--- |
| `[e.g., ADD COLUMN]` | `[table_name]` | `[count]` | `[Tier]` |

### 2. Violations & Mitigation
*(List any WARNING or CRITICAL violations here. Omit if SAFE.)*
- **Violation**: [Description of the issue, e.g., missing CONCURRENTLY]
- **Required Mitigation**: [How to fix it, e.g., Rewrite as CREATE INDEX CONCURRENTLY]

### 3. Verification & Rollback
- **Pre-flight Checks**: [List of checks performed]
- **Rollback Readiness**: [Confirm a `down` migration exists]
- **Post-Deploy Monitoring**: Recommended 15 minute observation on DB CPU.
```
