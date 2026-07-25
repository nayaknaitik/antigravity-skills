# Rollback Procedures

If a migration causes an incident, the following steps must be taken immediately.

1. **Identify the PID**: Find the stuck migration transaction ID or process ID.
2. **Kill the Process**: Terminate the transaction gracefully if possible, or kill the connection.
3. **Revert DDL**: Run the corresponding `down` migration script to revert the schema changes.
4. **Halt Application Rollout**: Ensure that any application code deployments relying on the new schema are instantly rolled back to the previous stable SHA.
5. **Post-Mortem**: Document the lock or timeout and update the decision table thresholds in `SKILL.md`.
