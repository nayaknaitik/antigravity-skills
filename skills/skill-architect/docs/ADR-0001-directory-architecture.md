# ADR-0001: Standardized 9-Directory AI Skill Architecture

- **Status**: Approved
- **Deciders**: AI Engineering Lead Architect
- **Date**: 2026-07-23

## Context
AI Skills previously suffered from inconsistent structures, monolithic prompts, missing tests, and lack of automated quality enforcement. A unified engineering framework is required to ensure all skills across the organization are production-grade, maintainable, versioned, and testable.

## Decision
We adopt a mandatory 9-directory structure for every AI Skill in the organization:
1. `references/` - Knowledge, API specs, domain guidelines.
2. `assets/` - Static media, diagrams, branding.
3. `scripts/` - Executable tooling, validators, generators.
4. `templates/` - Scaffolding code and markdown templates.
5. `tests/` - Unit tests, test runners, golden input/output fixtures.
6. `examples/` - Golden reference usage demonstrations.
7. `metadata/` - Machine-readable manifest (`skill.json`) and schemas.
8. `docs/` - Human engineering documentation (`USER_GUIDE.md`, `MAINTAINER_GUIDE.md`, `CHANGELOG.md`, ADRs).
9. `SKILL.md` - Primary AI agent instruction manual and state machine.

## Consequences
- **Positive**: Standardizes all skills, enables automated quality scoring (0-100), simplifies CI/CD integration, ensures high maintainability.
- **Negative**: Adds slight scaffolding overhead for trivial skills, mitigated entirely by `scripts/skill_generator.py`.
