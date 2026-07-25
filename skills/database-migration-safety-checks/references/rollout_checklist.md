# Validation-Before-Trust Rollout Checklist

Before trusting this skill with full autonomy in a CI/CD pipeline, the following phases MUST be completed.

- [ ] **Phase 1: Backtesting**
  - Run the skill against the last 50 historical database migrations in the repo.
  - Verify that it accurately flags the 3 known historical migrations that caused table locks.
- [ ] **Phase 2: Shadow Mode**
  - Integrate the skill into PRs as a non-blocking "dry run" comment only.
  - Have a Senior DBA manually review the skill's output for false positives and false negatives over a 2-week period.
- [ ] **Phase 3: Staged Rollout**
  - Enable blocking autonomy ONLY for `SAFE` tiered migrations.
  - Require manual overrides for `WARNING` and `CRITICAL`.
- [ ] **Phase 4: Feedback Loop**
  - Establish a monthly review of overridden PRs to refine the thresholds in the Decision Table.
