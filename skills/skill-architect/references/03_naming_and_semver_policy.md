# Naming Conventions, Versioning & Migration Policy

## 1. Naming Standards

### 1.1 Directory Naming
- **Skill Root Directory**: MUST use lower `kebab-case` matching the skill name defined in YAML frontmatter (e.g., `skill-architect`, `database-migration-architect`, `security-auditor`).
- **Standard Subdirectories**: MUST match the exact 8 lowercase names: `references`, `assets`, `scripts`, `templates`, `tests`, `examples`, `metadata`, `docs`. Custom subdirectories are forbidden.

### 1.2 File Naming Rules
- **Markdown Files**: Lower `kebab-case` with `.md` extension (e.g., `user-guide.md`, `quality-matrix.md`).
- **Python Scripts**: Lower `snake_case` with `.py` extension (e.g., `skill_validator.py`, `quality_scorer.py`).
- **Templates**: Lower `snake_case` or `kebab-case` with `.template` or `.j2` extension (e.g., `skill_md.template`, `requirements_template.md`).
- **Tests**: Prefixed with `test_` or suffixed with `_test.py` (e.g., `test_skill_validator.py`).
- **Schemas & Manifests**: Lower `snake_case` with `.json` or `.yaml` extension (e.g., `skill_manifest_schema.json`).

---

## 2. Semantic Versioning (SemVer 2.0.0)

Every AI Skill MUST maintain a formal version string in its YAML frontmatter and `metadata/skill.json` following `MAJOR.MINOR.PATCH`:

```yaml
version: 1.2.0
```

### 2.1 Version Number Increment Rules
1. **MAJOR Version (X.0.0)**:
   - Modifying required Input/Output schemas in a non-backwards-compatible manner.
   - Removing existing quality gates or breaking public automation contracts.
   - Restructuring core workflow state machines requiring upstream agent adjustments.
2. **MINOR Version (0.Y.0)**:
   - Adding new optional input parameters or optional output fields.
   - Adding new templates, scripts, or reference guidelines without breaking existing contracts.
   - Extending trigger rules or positive activation patterns.
3. **PATCH Version (0.0.Z)**:
   - Bug fixes in helper scripts (`scripts/*.py`).
   - Typo corrections in documentation or references.
   - Prompt tuning that improves determinism without altering input/output schemas.

---

## 3. Migration Strategy & Deprecation Lifecycle

When breaking changes (MAJOR version bumps) are introduced:

1. **Deprecation Notice**:
   - Mark deprecated skill versions in `metadata/skill.json` with `deprecated: true` and specify `replacement_version`.
   - Provide a migration path document in `docs/migration-vX-to-vY.md`.
2. **Backward Compatibility Bridge**:
   - Retain legacy input parameter alias mapping in `SKILL.md` for at least one MINOR cycle before removal.
3. **Automated Migration Scripts**:
   - Provide a Python script in `scripts/migrate_v1_to_v2.py` whenever automated schema transformation is possible.
