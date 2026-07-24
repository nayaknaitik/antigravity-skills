# Enterprise SDLC & AI Agent Workflow Integration

## 1. Skill Lifecycle & SDLC Alignment

AI Skills are treated as first-class engineering code. They participate in standard Software Development Lifecycle (SDLC) practices:

```
[ Research ] ➔ [ Architecture & Design ] ➔ [ Skill Generation ] ➔ [ Automated Quality Gate ]
                                                                             │
[ Production Release ]  [ Security & PR Review ]  [ Automated Testing ] ◄──┘
         │
         ▼
[ Maintenance & SemVer Deprecation ]
```

---

## 2. CI/CD Pipeline Integration

Every Pull Request modifying or creating a skill MUST trigger automated quality scoring and linting in CI/CD (GitHub Actions / GitLab CI / Jenkins):

```yaml
# Sample GitHub Action Step
name: AI Skill Quality Gate
on: [pull_request]
jobs:
  validate-skill:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run Skill Validator & Scorer
        run: |
          python3 .antigravity/skills/skill-architect/scripts/skill_validator.py --skill-path .antigravity/skills/target-skill
          python3 .antigravity/skills/skill-architect/scripts/quality_scorer.py --skill-path .antigravity/skills/target-skill --min-score 85
```

---

## 3. Human & AI Pair Programming Protocols

1. **Subagent Delegation**:
   - Complex multi-step skill generation tasks are split between orchestrators and subagents (`invoke_subagent`).
   - The `research` subagent conducts domain exploration, while the `self` or specialist subagent handles file scaffold creation and script execution.
2. **Quality Gate Blocking**:
   - No skill is merged into `main` if the score is below 85.
   - Failing tests or un-handled failure modes block automated release pipelines.
3. **Artifact Handoff**:
   - The skill outputs structured markdown artifacts for architectural reviews, pull request summaries, and security audits.
