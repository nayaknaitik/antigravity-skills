# Maintainer Guide: Rust Engineering Skill

## 1. Directory Structure & Governance
This skill adheres strictly to the 9-directory Skill Architect standard:
- `SKILL.md`: Core instruction set, activation rules, state machine, and reasoning strategy.
- `references/`: Detailed reference documentation covering Cargo workspaces, Tokio, errors, concurrency, databases, and unsafe Rust rules.
- `templates/`: Production templates (Cargo workspace, Axum server, thiserror, SQLx repository).
- `examples/`: Worked reference implementations (Cancellation shutdown worker, lock-free sequence bus).
- `scripts/`: Code validator engine (`rust_code_validator.py`).
- `tests/`: Automated unit tests.
- `docs/`: User Guide, Maintainer Guide, Changelog.
- `metadata/`: `skill.json` manifest.

---

## 2. Quality Scoring & Verification
To run structural validation and score quality:
```bash
python3 .antigravity/skills/skill-architect/scripts/skill_validator.py --skill-path .antigravity/skills/rust-engineering
python3 .antigravity/skills/skill-architect/scripts/quality_scorer.py --skill-path .antigravity/skills/rust-engineering
```
Target Quality Score MUST be $\ge 85$ (Grade A / A+).
