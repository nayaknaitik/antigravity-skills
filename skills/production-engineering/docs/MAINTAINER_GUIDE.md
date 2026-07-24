# Production Engineering Skill - Maintainer Guide

## Updating Engineering Standards
As our engineering practices evolve:
1. **Reference Docs**: Update files under `references/` when industry standards (OpenTelemetry, CNCF, AWS Builders Library) evolve.
2. **Quality Gates**: Ensure quality scorer target remains >= 85.
3. **Automated Verification**: Keep `scripts/production_readiness_checker.py` and `scripts/api_compatibility_checker.py` synchronized with new standards.
4. **SemVer Versioning**: Increment minor version for new standards and major for breaking architectural shifts.
