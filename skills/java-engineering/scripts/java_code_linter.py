#!/usr/bin/env python3
"""
Java 21 & Spring Boot 3 Code Linter & Architectural Auditor
Audits Java source files and Spring Boot project structures against organizational standards.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

def audit_java_file(file_path: Path) -> list:
    issues = []
    content = file_path.read_text(encoding="utf-8")
    lower = content.lower()

    # Rule 1: Anti-pattern - System.out.println
    if "system.out.print" in lower:
        issues.append(f"{file_path.name}: Avoid System.out.println; use SLF4J Logger.")

    # Rule 2: Anti-pattern - Null returned or Optional.get()
    if ".get()" in content and "optional" in lower:
        issues.append(f"{file_path.name}: Avoid calling Optional.get() directly; use orElseThrow().")

    # Rule 3: Anti-pattern - Field injection
    if "@autowired" in lower and ("private " in lower or "protected " in lower):
        if not ("constructor" in lower or "public " + file_path.stem in content):
            issues.append(f"{file_path.name}: Avoid field injection (@Autowired on fields); use constructor injection.")

    # Rule 4: Anti-pattern - Swallowing exception
    if "catch (exception " in lower or "catch(exception " in lower:
        if "// ignore" in lower or "catch (exception e) {}" in content:
            issues.append(f"{file_path.name}: Never swallow exceptions; preserve stack trace or log.")

    return issues

def audit_project(project_path: str) -> dict:
    path = Path(project_path).resolve()
    if not path.exists():
        return {"error": f"Path '{project_path}' does not exist.", "status": "FAILED", "score": 0}

    java_files = list(path.glob("**/*.java"))
    if not java_files:
        return {"file_count": 0, "issues": ["No .java files found"], "score": 100, "status": "APPROVED"}

    all_issues = []
    for jf in java_files:
        issues = audit_java_file(jf)
        all_issues.extend(issues)

    score = max(0, 100 - (len(all_issues) * 5))
    return {
        "project": str(path),
        "java_file_count": len(java_files),
        "issues_count": len(all_issues),
        "issues": all_issues,
        "score": score,
        "status": "APPROVED" if score >= 85 else "REJECTED"
    }

def main():
    parser = argparse.ArgumentParser(description="Java 21 & Spring Boot Architectural Linter")
    parser.add_argument("--path", required=True, help="Path to Java project or file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    result = audit_project(args.path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"=== Java Architectural Audit Report ===")
        print(f"Project: {result.get('project')}")
        print(f"Files Audited: {result.get('java_file_count')}")
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
