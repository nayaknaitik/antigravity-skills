#!/usr/bin/env python3
"""
Go Architectural & Idiomatic Linter
Audits Go source files against Uber Go Style Guide, Effective Go, and organizational quality gates.
"""

import sys
import os
import json
import argparse
from pathlib import Path

def audit_go_file(file_path: Path) -> list:
    issues = []
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Rule 1: Anti-pattern - fmt.Println in production
    for i, line in enumerate(lines, 1):
        if "fmt.print" in line.lower() and not file_path.name.endswith("_test.go") and "main.go" not in file_path.name:
            issues.append(f"{file_path.name}:{i}: Avoid fmt.Println; use log/slog structured logger.")

    # Rule 2: Anti-pattern - panic() usage
    for i, line in enumerate(lines, 1):
        if "panic(" in line and not file_path.name.endswith("_test.go"):
            if "unrecoverable" not in line.lower():
                issues.append(f"{file_path.name}:{i}: Avoid panic() in production code; return explicit error instead.")

    # Rule 3: Anti-pattern - Ignored errors (_ = funcCallReturningErr)
    for i, line in enumerate(lines, 1):
        if "_ = " in line and ("err" in line or "Close" in line or "Exec" in line):
            issues.append(f"{file_path.name}:{i}: Do not ignore returned errors using '_ ='. Handle or log explicitly.")

    # Rule 4: Anti-pattern - Missing context parameter in IO function
    if "func " in content and "Repository" in file_path.name:
        if "ctx context.Context" not in content:
            issues.append(f"{file_path.name}: Repository functions MUST accept context.Context as first parameter.")

    return issues

def audit_project(project_path: str) -> dict:
    path = Path(project_path).resolve()
    if not path.exists():
        return {"error": f"Path '{project_path}' does not exist.", "status": "FAILED", "score": 0}

    go_files = list(path.glob("**/*.go"))
    if not go_files:
        return {"file_count": 0, "issues": ["No .go files found"], "score": 100, "status": "APPROVED"}

    all_issues = []
    for gf in go_files:
        issues = audit_go_file(gf)
        all_issues.extend(issues)

    score = max(0, 100 - (len(all_issues) * 5))
    return {
        "project": str(path),
        "go_file_count": len(go_files),
        "issues_count": len(all_issues),
        "issues": all_issues,
        "score": score,
        "status": "APPROVED" if score >= 85 else "REJECTED"
    }

def main():
    parser = argparse.ArgumentParser(description="Go Architectural Linter")
    parser.add_argument("--path", required=True, help="Path to Go project or file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    result = audit_project(args.path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"=== Go Architectural Audit Report ===")
        print(f"Project: {result.get('project')}")
        print(f"Files Audited: {result.get('go_file_count')}")
        print(f"Score:   {result.get('score')}/100")
        print(f"Status:  {result.get('status')}\n")

        if result.get("issues"):
            print("Issues Found:")
            for issue in result["issues"]:
                print(f"  [X] {issue}")
        else:
            print("  [✓] Zero architectural violations detected.")

        sys.exit(0 if result.get("score", 0) >= 85 else 1)

if __name__ == "__main__":
    main()
