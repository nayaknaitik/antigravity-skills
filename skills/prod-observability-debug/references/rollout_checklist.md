# Validation-Before-Trust Rollout Checklist

Before trusting this skill with full autonomy in a production environment, complete the following rollout phases:

- [ ] **Phase 1: Replay & Backtesting**
  - Feed the skill data from 3 past resolved production incidents.
  - Verify that the skill's hypotheses correctly identify the historic root cause in at least 2 of the 3 cases.
- [ ] **Phase 2: Shadow Mode**
  - Deploy the skill to ingest live alerts and generate Incident Reports (hypotheses + recommended actions).
  - The skill is **strictly read-only** and posts its reports to a quiet `#bot-shadow-testing` channel.
  - Human engineers review the reports for 2 weeks to assess diagnostic accuracy and false-positive rates.
- [ ] **Phase 3: Staged Pilot**
  - Enable autonomous `AUTO-FIX` actions ONLY for one non-critical, isolated service in the staging environment.
  - Verify closed-loop verification protocols catch any failed fixes.
- [ ] **Phase 4: Full Rollout & Feedback Loop**
  - Enable `AUTO-FIX` in production for specific Whitelisted actions only.
  - Establish a bi-weekly review meeting where engineers grade the skill's incident reports, adjusting `check_thresholds.md` to tune out noise and expand the allowlist.
