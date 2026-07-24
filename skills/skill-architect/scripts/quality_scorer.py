#!/usr/bin/env python3
"""
AI Skill Quality Scorer & Evaluation Engine
Evaluates an AI Skill across 10 quality dimensions and generates a weighted score (0-100),
grade classification, and actionable feedback report.
"""

import sys
import os
import json
import argparse
from pathlib import Path

DIMENSIONS = {
    "D1_STRUCTURE": {"name": "Directory & Structure Completeness", "weight": 10},
    "D2_METADATA": {"name": "Frontmatter & Metadata Integrity", "weight": 10},
    "D3_ACTIVATION": {"name": "Activation & Trigger Precision", "weight": 10},
    "D4_SCHEMAS": {"name": "Input/Output Schema Definition", "weight": 10},
    "D5_WORKFLOW": {"name": "Workflow State Machine & Strategy", "weight": 10},
    "D6_QUALITY_GATES": {"name": "Quality Gates & Failure Handling", "weight": 10},
    "D7_TEMPLATES": {"name": "Template Scaffolding Coverage", "weight": 10},
    "D8_TESTING": {"name": "Test Suite & Verification Logic", "weight": 10},
    "D9_EXAMPLES": {"name": "Golden Examples & Demonstrations", "weight": 10},
    "D10_DOCS": {"name": "Human & Machine Documentation", "weight": 10},
}

REQUIRED_DIRECTORIES = ["references", "assets", "scripts", "templates", "tests", "examples", "metadata", "docs"]

def evaluate_skill(skill_path: str) -> dict:
    path = Path(skill_path).resolve()
    if not path.is_dir():
        return {"error": f"Path '{skill_path}' is not a directory", "score": 0, "grade": "F"}

    scores = {}
    feedback = {}

    # D1: Structure Check
    d1_score = 10
    d1_issues = []
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        d1_score -= 5
        d1_issues.append("Missing root SKILL.md file")
    
    for folder in REQUIRED_DIRECTORIES:
        if not (path / folder).is_dir():
            d1_score -= 1
            d1_issues.append(f"Missing subdirectory: {folder}/")
    scores["D1_STRUCTURE"] = max(0, d1_score)
    feedback["D1_STRUCTURE"] = d1_issues or ["All standard directories present"]

    # Read SKILL.md content if exists
    skill_content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""

    # D2: Metadata Check
    d2_score = 10
    d2_issues = []
    has_frontmatter = skill_content.startswith("---")
    if not has_frontmatter:
        d2_score -= 5
        d2_issues.append("SKILL.md missing YAML frontmatter delimiters ('---')")
    else:
        for field in ["name:", "description:", "version:"]:
            if field not in skill_content.split("---")[1]:
                d2_score -= 2
                d2_issues.append(f"Frontmatter missing field '{field[:-1]}'")
    
    meta_json = path / "metadata" / "skill.json"
    if not meta_json.exists():
        d2_score -= 2
        d2_issues.append("Missing metadata/skill.json manifest")
    scores["D2_METADATA"] = max(0, d2_score)
    feedback["D2_METADATA"] = d2_issues or ["Frontmatter and metadata manifest valid"]

    # D3: Activation & Trigger Precision
    d3_score = 10
    d3_issues = []
    content_lower = skill_content.lower()
    if "activation rules" not in content_lower and "trigger" not in content_lower:
        d3_score -= 5
        d3_issues.append("SKILL.md lacks explicit activation/trigger section")
    if "negative" not in content_lower and "do not activate" not in content_lower:
        d3_score -= 3
        d3_issues.append("SKILL.md lacks negative activation constraints")
    scores["D3_ACTIVATION"] = max(0, d3_score)
    feedback["D3_ACTIVATION"] = d3_issues or ["Activation rules and negative triggers specified"]

    # D4: Input/Output Schemas
    d4_score = 10
    d4_issues = []
    if "input" not in content_lower:
        d4_score -= 4
        d4_issues.append("SKILL.md lacks structured input specification")
    if "output" not in content_lower:
        d4_score -= 4
        d4_issues.append("SKILL.md lacks structured output specification")
    scores["D4_SCHEMAS"] = max(0, d4_score)
    feedback["D4_SCHEMAS"] = d4_issues or ["Input and output schemas defined"]

    # D5: Workflow State Machine
    d5_score = 10
    d5_issues = []
    if "workflow" not in content_lower and "step" not in content_lower:
        d5_score -= 5
        d5_issues.append("SKILL.md lacks step-by-step workflow state machine")
    if "decision" not in content_lower and "strategy" not in content_lower:
        d5_score -= 3
        d5_issues.append("SKILL.md lacks decision process logic")
    scores["D5_WORKFLOW"] = max(0, d5_score)
    feedback["D5_WORKFLOW"] = d5_issues or ["Workflow state machine and reasoning strategy specified"]

    # D6: Quality Gates & Failure Handling
    d6_score = 10
    d6_issues = []
    if "quality gate" not in content_lower and "validation" not in content_lower:
        d6_score -= 5
        d6_issues.append("SKILL.md lacks quality gate specifications")
    if "failure" not in content_lower and "error" not in content_lower:
        d6_score -= 4
        d6_issues.append("SKILL.md lacks failure condition runbooks")
    scores["D6_QUALITY_GATES"] = max(0, d6_score)
    feedback["D6_QUALITY_GATES"] = d6_issues or ["Quality gates and failure runbooks defined"]

    # D7: Templates Coverage
    d7_score = 10
    d7_issues = []
    template_files = list((path / "templates").glob("*")) if (path / "templates").is_dir() else []
    if len(template_files) == 0:
        d7_score -= 10
        d7_issues.append("templates/ directory is empty")
    elif len(template_files) < 3:
        d7_score -= 4
        d7_issues.append(f"Only {len(template_files)} template(s) found in templates/, expected at least 3")
    scores["D7_TEMPLATES"] = max(0, d7_score)
    feedback["D7_TEMPLATES"] = d7_issues or [f"Found {len(template_files)} template files in templates/"]

    # D8: Testing & Verification
    d8_score = 10
    d8_issues = []
    test_files = list((path / "tests").glob("*")) if (path / "tests").is_dir() else []
    if len(test_files) == 0:
        d8_score -= 10
        d8_issues.append("tests/ directory is empty")
    scores["D8_TESTING"] = max(0, d8_score)
    feedback["D8_TESTING"] = d8_issues or [f"Found {len(test_files)} test/fixture files in tests/"]

    # D9: Golden Examples
    d9_score = 10
    d9_issues = []
    example_files = list((path / "examples").glob("*")) if (path / "examples").is_dir() else []
    if len(example_files) == 0:
        d9_score -= 10
        d9_issues.append("examples/ directory is empty")
    scores["D9_EXAMPLES"] = max(0, d9_score)
    feedback["D9_EXAMPLES"] = d9_issues or [f"Found {len(example_files)} reference examples in examples/"]

    # D10: Documentation
    d10_score = 10
    d10_issues = []
    docs_dir = path / "docs"
    if docs_dir.is_dir():
        for doc in ["USER_GUIDE.md", "MAINTAINER_GUIDE.md", "CHANGELOG.md"]:
            if not (docs_dir / doc).exists():
                d10_score -= 3
                d10_issues.append(f"Missing docs/{doc}")
    else:
        d10_score = 0
        d10_issues.append("docs/ directory missing")
    scores["D10_DOCS"] = max(0, d10_score)
    feedback["D10_DOCS"] = d10_issues or ["All standard documentation files present"]

    # Total Score Calculation
    total_score = sum(scores.values())

    if total_score >= 95:
        grade = "A+"
        status = "Approved (Exemplary)"
    elif total_score >= 85:
        grade = "A"
        status = "Approved (Production Grade)"
    elif total_score >= 70:
        grade = "B"
        status = "Blocked (Needs Improvement)"
    elif total_score >= 50:
        grade = "C"
        status = "Blocked (Non-Compliant Draft)"
    else:
        grade = "F"
        status = "Rejected (Critical Fail)"

    return {
        "skill_name": path.name,
        "total_score": total_score,
        "grade": grade,
        "status": status,
        "dimension_scores": scores,
        "feedback": feedback
    }

def main():
    parser = argparse.ArgumentParser(description="AI Skill Quality Scorer")
    parser.add_argument("--skill-path", required=True, help="Path to the skill directory to score")
    parser.add_argument("--min-score", type=int, default=85, help="Minimum score required to pass quality gate")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    report = evaluate_skill(args.skill_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"==================================================")
        print(f"   AI SKILL QUALITY EVALUATION REPORT: {report.get('skill_name')}")
        print(f"==================================================")
        print(f"Quality Score: {report.get('total_score')}/100")
        print(f"Grade:        {report.get('grade')}")
        print(f"Status:       {report.get('status')}")
        print(f"--------------------------------------------------\n")

        print("Dimension Scores & Feedback:")
        for dim_id, meta in DIMENSIONS.items():
            score = report['dimension_scores'].get(dim_id, 0)
            items = report['feedback'].get(dim_id, [])
            print(f"[{score:2d}/10] {meta['name']} ({dim_id})")
            for item in items:
                prefix = "  ✓" if "present" in item.lower() or "valid" in item.lower() or "defined" in item.lower() or "found" in item.lower() or "specified" in item.lower() or "includes" in item.lower() else "  X"
                print(f"{prefix} {item}")
            print()

        passed = report.get('total_score', 0) >= args.min_score
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
