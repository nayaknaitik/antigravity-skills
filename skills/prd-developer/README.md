# PRD Developer

Enterprise-grade AI skill architecture for transforming vague ideas into production-ready Product Requirement Documents (PRDs).

## Architecture Principles
1. **Single Responsibility**: Every markdown file solves exactly ONE problem.
2. **Context Efficiency**: Extreme token optimization via lazy loading.
3. **No Duplication**: Shared knowledge is referenced, not repeated.
4. **Reasoning Rigor**: Facts, assumptions, and unknowns are strictly separated.

## Directory Structure
- `skill.yaml`: The orchestrator and routing rule definition.
- `SKILL.md`: Antigravity entry point.
- `docs/`: Highly cohesive, single-responsibility markdown files.
- `templates/`: Reusable markdown structures for final output.

To use this skill, the agent routes via `skill.yaml` and loads only the required document for the active workflow step.
