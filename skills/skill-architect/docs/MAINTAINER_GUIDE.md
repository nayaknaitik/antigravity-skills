# Skill Architect Maintainer Guide

## Overview
This document provides guidelines for maintainers responsible for updating `skill-architect` itself, modifying quality evaluation rules, or updating standardized templates.

---

## Modifying Evaluation Rules in `quality_scorer.py`
1. Evaluation dimensions are defined in `scripts/quality_scorer.py` under `DIMENSIONS`.
2. Total weight must sum to 100 points across all dimensions.
3. If new mandatory files or checks are added:
   - Update `references/04_quality_scoring_specification.md`.
   - Update `tests/test_skill_validator.py` to ensure unit test suite covers the new check.

---

## Testing & Quality Gate Verification
Before releasing a new version of `skill-architect`:

```bash
# Run unit test suite
python3 .antigravity/skills/skill-architect/tests/test_skill_validator.py

# Validate skill-architect itself
python3 .antigravity/skills/skill-architect/scripts/skill_validator.py \
  --skill-path ".antigravity/skills/skill-architect"

# Score skill-architect itself
python3 .antigravity/skills/skill-architect/scripts/quality_scorer.py \
  --skill-path ".antigravity/skills/skill-architect" --min-score 95
```
