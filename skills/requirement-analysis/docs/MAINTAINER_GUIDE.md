# Requirement Analysis Skill Maintainer Guide

## 1. Quality Gate Verification
Maintainers must verify that `requirement-analysis` passes the root Skill Architect validator and quality scorer before tagging any releases:

```bash
# Validate structure
python3 .antigravity/skills/skill-architect/scripts/skill_validator.py \
  --skill-path .antigravity/skills/requirement-analysis

# Score quality (Target score >= 85)
python3 .antigravity/skills/skill-architect/scripts/quality_scorer.py \
  --skill-path .antigravity/skills/requirement-analysis --min-score 85

# Execute unit tests
python3 .antigravity/skills/requirement-analysis/tests/test_ambiguity_checker.py
```
