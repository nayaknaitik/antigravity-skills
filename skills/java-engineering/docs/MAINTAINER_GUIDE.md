# Java Engineering Skill - Maintainer Guide

## Updating the Skill
1. **References**: Update `references/` when new Java LTS versions (e.g. Java 25) or Spring Boot major releases occur.
2. **Quality Gates**: Run `python3 scripts/java_code_linter.py --path examples/` to verify examples.
3. **SemVer**: Maintain Semantic Versioning 2.0.0 in `metadata/skill.json`.
