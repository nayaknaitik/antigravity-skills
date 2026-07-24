#!/usr/bin/env python3
"""
Automated Skill Generator Engine
Scaffolds a new, production-compliant AI Skill directory structure complete with
all 9 mandatory subdirectories, YAML frontmatter, starter templates, metadata manifest, and tests.
"""

import sys
import os
import json
import argparse
from pathlib import Path

STANDARD_FOLDERS = [
    "references",
    "assets",
    "scripts",
    "templates",
    "tests",
    "examples",
    "metadata",
    "docs"
]

SKILL_MD_TEMPLATE = """---
name: {skill_name}
description: {skill_description}
version: 1.0.0
author: AI Engineering Architect
tags: [{skill_name}, ai-engineering, production-skill]
---

# {skill_title} Skill Instruction Set

## 1. Purpose
{skill_description}

## 2. Activation Rules & Trigger Patterns
- **Positive Triggers**:
  - Activate when requested to perform {skill_name} operations.
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
"""

def generate_skill(name: str, description: str, output_dir: str) -> str:
    skill_slug = name.lower().strip().replace(" ", "-")
    target_path = Path(output_dir).resolve() / skill_slug

    print(f"Scaffolding new AI Skill: '{skill_slug}' at {target_path}...")
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. Create subdirectories
    for folder in STANDARD_FOLDERS:
        (target_path / folder).mkdir(exist_ok=True)
        # Add .gitkeep to ensure empty dirs are tracked
        (target_path / folder / ".gitkeep").touch()

    # 2. Write SKILL.md
    skill_title = name.replace("-", " ").replace("_", " ").title()
    skill_md_content = SKILL_MD_TEMPLATE.format(
        skill_name=skill_slug,
        skill_description=description,
        skill_title=skill_title
    )
    (target_path / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

    # 3. Write metadata/skill.json
    manifest = {
        "name": skill_slug,
        "version": "1.0.0",
        "description": description,
        "author": "AI Engineering Architect",
        "tags": [skill_slug, "ai-engineering"],
        "dependencies": {
            "mcp_servers": [],
            "python_packages": [],
            "scripts": []
        },
        "quality_score_target": 85
    }
    (target_path / "metadata" / "skill.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # 4. Write initial docs
    (target_path / "docs" / "USER_GUIDE.md").write_text(f"# User Guide for {skill_title}\n\nHow to activate and run the {skill_slug} skill.\n", encoding="utf-8")
    (target_path / "docs" / "MAINTAINER_GUIDE.md").write_text(f"# Maintainer Guide for {skill_title}\n\nHow to update, test, and version the {skill_slug} skill.\n", encoding="utf-8")
    (target_path / "docs" / "CHANGELOG.md").write_text(f"# Changelog\n\n## [1.0.0] - Initial Release\n- Initial scaffolding of {skill_slug}.\n", encoding="utf-8")

    # 5. Write reference placeholder
    (target_path / "references" / "01_overview.md").write_text(f"# {skill_title} Reference Guide\n\nDomain rules and specifications.\n", encoding="utf-8")

    # 6. Write template placeholder
    (target_path / "templates" / "default_template.md").write_text(f"# {skill_title} Template\n", encoding="utf-8")

    # 7. Write test placeholder
    (target_path / "tests" / "test_skill.py").write_text(f"def test_{skill_slug.replace('-', '_')}():\n    assert True\n", encoding="utf-8")

    # 8. Write example placeholder
    (target_path / "examples" / "sample_usage.md").write_text(f"# Sample Usage of {skill_title}\n", encoding="utf-8")

    print(f"✓ Skill '{skill_slug}' successfully generated!")
    return str(target_path)

def main():
    parser = argparse.ArgumentParser(description="Automated AI Skill Generator")
    parser.add_argument("--name", required=True, help="Name of the new skill (e.g. database-migration)")
    parser.add_argument("--description", required=True, help="Description of the skill's purpose")
    parser.add_argument("--output-dir", default=".", help="Base directory where skill folder will be created")
    args = parser.parse_args()

    generate_skill(args.name, args.description, args.output_dir)

if __name__ == "__main__":
    main()
