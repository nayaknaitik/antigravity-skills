#!/usr/bin/env python3
"""
AI Skill Structural & Schema Validator
Validates that an AI Skill directory complies with organizational directory standards,
YAML frontmatter requirements, and JSON schema definitions.
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path

REQUIRED_DIRECTORIES = [
    "references",
    "assets",
    "scripts",
    "templates",
    "tests",
    "examples",
    "metadata",
    "docs"
]

REQUIRED_DOCS = [
    "docs/USER_GUIDE.md",
    "docs/MAINTAINER_GUIDE.md",
    "docs/CHANGELOG.md"
]

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    
    yaml_text = parts[1]
    metadata = {}
    for line in yaml_text.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata

def validate_skill(skill_path: str) -> dict:
    """Runs structural and content validation on a target skill directory."""
    path = Path(skill_path).resolve()
    errors = []
    warnings = []
    passed_checks = []

    if not path.is_dir():
        return {
            "valid": False,
            "skill_name": path.name,
            "errors": [f"Target path '{skill_path}' is not a directory."],
            "warnings": [],
            "passed_checks": []
        }

    # 1. Check SKILL.md
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing required file: SKILL.md")
    else:
        passed_checks.append("SKILL.md exists")
        content = skill_md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)
        
        for required_key in ["name", "description", "version"]:
            if required_key not in frontmatter:
                errors.append(f"SKILL.md frontmatter missing required field: '{required_key}'")
            else:
                passed_checks.append(f"SKILL.md frontmatter includes '{required_key}'")

    # 2. Check 8 Standard Directories
    for folder in REQUIRED_DIRECTORIES:
        dir_path = path / folder
        if not dir_path.exists() or not dir_path.is_dir():
            errors.append(f"Missing required subdirectory: {folder}/")
        else:
            passed_checks.append(f"Directory {folder}/ exists")

    # 3. Check Docs files
    for doc in REQUIRED_DOCS:
        doc_path = path / doc
        if not doc_path.exists():
            warnings.append(f"Recommended documentation file missing: {doc}")
        else:
            passed_checks.append(f"Documentation file {doc} exists")

    # 4. Check metadata/skill.json
    meta_json = path / "metadata" / "skill.json"
    if not meta_json.exists():
        warnings.append("Missing metadata manifest: metadata/skill.json")
    else:
        try:
            with open(meta_json, "r", encoding="utf-8") as f:
                json.load(f)
            passed_checks.append("metadata/skill.json is valid JSON")
        except Exception as e:
            errors.append(f"metadata/skill.json contains invalid JSON: {str(e)}")

    return {
        "valid": len(errors) == 0,
        "skill_name": path.name,
        "errors": errors,
        "warnings": warnings,
        "passed_checks": passed_checks
    }

def main():
    parser = argparse.ArgumentParser(description="AI Skill Structural & Schema Validator")
    parser.add_argument("--skill-path", required=True, help="Path to the skill directory to validate")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = validate_skill(args.skill_path)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"=== Skill Validation Report: {results['skill_name']} ===")
        print(f"Status: {'PASSED' if results['valid'] else 'FAILED'}\n")
        
        print("Passed Checks:")
        for check in results["passed_checks"]:
            print(f"  [✓] {check}")
            
        if results["warnings"]:
            print("\nWarnings:")
            for warn in results["warnings"]:
                print(f"  [!] {warn}")

        if results["errors"]:
            print("\nErrors:")
            for err in results["errors"]:
                print(f"  [X] {err}")
                
        sys.exit(0 if results["valid"] else 1)

if __name__ == "__main__":
    main()
