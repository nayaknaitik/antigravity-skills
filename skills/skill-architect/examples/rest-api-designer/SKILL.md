---
name: rest-api-designer
description: Production-grade REST API design and OpenAPI specification generator skill
version: 1.0.0
author: AI Engineering Architect
tags: [rest-api-designer, ai-engineering, production-skill]
---

# Rest Api Designer Skill Instruction Set

## 1. Purpose
Production-grade REST API design and OpenAPI specification generator skill

## 2. Activation Rules & Trigger Patterns
- **Positive Triggers**:
  - Activate when requested to perform rest-api-designer operations.
- **Negative Triggers**:
  - Do NOT activate for general unrelated inquiries.
- **Context Constraints**:
  - Requires target workspace directory and explicit user parameters.

## 3. Inputs & Context Schemas
| Parameter Name | Data Type | Required? | Description | Validation Rule |
| :--- | :--- | :---: | :--- | :--- |
| `target_path` | String | Yes | Absolute path to target workspace | Path must exist on filesystem |

## 4. Outputs & Artifact Specifications
- **Output Artifacts**: Structured Markdown report.
- **Filesystem Modifications**: Target files generated or edited in place.

## 5. End-to-End Workflow State Machine
1. **INIT**: Read input parameters and inspect workspace.
2. **RESEARCH**: Inspect references/ files for domain specifications.
3. **PLAN**: Formulate execution steps and present to user.
4. **EXECUTE**: Perform file updates or code generation.
5. **VERIFY**: Run verification tests and quality checks.
6. **HANDOFF**: Present final summary and point to created artifacts.

## 6. Decision Process & Reasoning Strategy
- Follow defensive execution: inspect existing files before mutating.
- Validate syntax and schemas prior to claiming success.

## 7. Quality Gates & Validation
- Run validator script: `python3 scripts/skill_validator.py`
- Run quality scorer: `python3 scripts/quality_scorer.py --min-score 85`

## 8. Failure Conditions & Recovery Runbook
| Failure Mode | Root Cause | Recovery Action |
| :--- | :--- | :--- |
| File Not Found | Path mismatch | Prompt user for correct path |
| Schema Error | Invalid JSON | Re-generate using schema template |

## 9. Pre-Commit Review Checklist
- [ ] Frontmatter valid
- [ ] References up to date
- [ ] Tests passing
- [ ] Quality score >= 85
