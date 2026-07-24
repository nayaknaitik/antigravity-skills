# Skill Architect User Guide

## Overview
`skill-architect` is the root skill of our engineering organization. It automates the end-to-end design, generation, validation, scoring, and release of all new AI Skills.

---

## Quick Start: Generating a New Skill

To generate a new AI Skill adhering to enterprise standards:

```bash
python3 .antigravity/skills/skill-architect/scripts/skill_generator.py \
  --name "database-migration-architect" \
  --description "Automates schema migration, SQL generation, and rollback scripts" \
  --output-dir ".antigravity/skills"
```

This creates a new folder `.antigravity/skills/database-migration-architect` with all 9 mandatory subdirectories populated.

---

## Validating an Existing Skill

```bash
python3 .antigravity/skills/skill-architect/scripts/skill_validator.py \
  --skill-path ".antigravity/skills/database-migration-architect"
```

---

## Running Quality Scoring Gate

```bash
python3 .antigravity/skills/skill-architect/scripts/quality_scorer.py \
  --skill-path ".antigravity/skills/database-migration-architect" \
  --min-score 85
```

---

## Key Rules for Skill Authors
1. **Never edit directory structure manually**: Always keep the 9 standard directories (`references/`, `assets/`, `scripts/`, `templates/`, `tests/`, `examples/`, `metadata/`, `docs/`).
2. **Strict SemVer**: Always bump version numbers according to Semantic Versioning 2.0.0 guidelines.
3. **Quality Gate Requirement**: Skills must score **85 or higher** before submitting a Pull Request.
