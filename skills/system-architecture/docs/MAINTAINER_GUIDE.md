# Maintainer Guide: System Architecture Skill

## 1. Directory & Code Structure
This skill follows the strict 9-directory Skill Architect standard:
- `SKILL.md`: Root instruction set and state machine.
- `references/`: Reference documentation for patterns, trading systems, AI architectures, distributed systems, and security.
- `templates/`: Production templates for HLD, LLD, ADR, trade-offs, and architecture checklists.
- `examples/`: Worked reference examples (Trading platform, OMS, Risk engine, AI agent platform).
- `scripts/`: Automated validation engine (`architecture_validator.py`).
- `tests/`: Automated unit tests.
- `docs/`: User, Maintainer, and Changelog documentation.
- `metadata/`: Machine-readable `skill.json` manifest.

---

## 2. Testing & Quality Scoring
To run structural validation and score quality:
```bash
python3 .antigravity/skills/skill-architect/scripts/skill_validator.py --skill-path .antigravity/skills/system-architecture
python3 .antigravity/skills/skill-architect/scripts/quality_scorer.py --skill-path .antigravity/skills/system-architecture
```
Target Quality Score MUST be $\ge 85$ (Grade A / A+).
