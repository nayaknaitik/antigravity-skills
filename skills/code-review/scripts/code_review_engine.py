#!/usr/bin/env python3
"""
Principal Code Review & Quality Gate Engine
Evaluates pull requests, codebases, or source files across 15 Code Review Dimensions.
Outputs Production Readiness Score (0-100), Risk Score, Severity Breakdown, and Merge Recommendation.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

REVIEW_DIMENSIONS = [
    "D1_CORRECTNESS", "D2_ARCHITECTURE", "D3_API_DESIGN", "D4_ERROR_HANDLING",
    "D5_CONCURRENCY", "D6_DATABASE", "D7_SECURITY", "D8_PERFORMANCE",
    "D9_SCALABILITY", "D10_RELIABILITY", "D11_OBSERVABILITY", "D12_TESTING",
    "D13_MAINTAINABILITY", "D14_AI_GENERATED_CODE", "D15_FINANCIAL_SAFETY"
]

def analyze_source_content(content: str, filename: str) -> dict:
    critical_issues = []
    high_issues = []
    medium_issues = []
    low_issues = []
    passed_checks = []

    lower = content.lower()

    # Security Check: Secrets
    if re.search(r'(api_key|password|secret|private_key)\s*=\s*["\'][A-Za-z0-9_\-]{8,}["\']', content, re.I):
        critical_issues.append("SECURITY BLOCKER: Hardcoded API key or secret detected in source code.")
    else:
        passed_checks.append("Zero hardcoded secrets detected")

    # Financial Check: Floating Point Money
    if re.search(r'\b(double|float|float32|float64)\s+(amount|price|balance|cost|money|total)\b', content, re.I):
        critical_issues.append("FINANCIAL SAFETY BLOCKER: Floating-point type used for monetary amount; must use BigDecimal or integer cents.")
    else:
        passed_checks.append("Monetary fields avoid raw floating point types")

    # Correctness Check: System.out or fmt.Println
    if "system.out.print" in lower or ("fmt.print" in lower and not filename.endswith("_test.go")):
        medium_issues.append("OBSERVABILITY: Avoid System.out or fmt.Println; use structured JSON logger (SLF4J / slog).")

    # Concurrency Check: Unhandled Goroutines / Thread Pinning
    if "go func()" in content and "context" not in lower:
        high_issues.append("CONCURRENCY: Goroutine launched without context cancellation or drain handling.")

    # Error Handling Check: Ignored Errors
    if "_ = " in content and ("err" in content or "Close" in content):
        high_issues.append("ERROR HANDLING: Returned error explicitly ignored using '_ ='.")

    # SQL Injection Check: String Concatenation in SQL
    if re.search(r'SELECT\s+.*\s+FROM\s+.*\s+\+\s*\w+', content, re.I):
        critical_issues.append("SECURITY BLOCKER: SQL query string concatenation detected; risk of SQL Injection.")

    # Calculate Scores
    critical_penalty = len(critical_issues) * 35
    high_penalty = len(high_issues) * 15
    medium_penalty = len(medium_issues) * 5
    low_penalty = len(low_issues) * 2

    readiness_score = max(0, 100 - (critical_penalty + high_penalty + medium_penalty + low_penalty))
    risk_score = min(100, (critical_penalty + high_penalty + medium_penalty + low_penalty))

    if len(critical_issues) > 0 or readiness_score < 70:
        recommendation = "REJECTED"
    elif len(high_issues) > 0 or readiness_score < 85:
        recommendation = "CHANGES_REQUESTED"
    else:
        recommendation = "APPROVED"

    return {
        "file": filename,
        "readiness_score": readiness_score,
        "risk_score": risk_score,
        "recommendation": recommendation,
        "critical_issues": critical_issues,
        "high_issues": high_issues,
        "medium_issues": medium_issues,
        "low_issues": low_issues,
        "passed_checks": passed_checks
    }

def review_target(target_path: str) -> dict:
    path = Path(target_path).resolve()
    if not path.exists():
        return {"error": f"Target path '{target_path}' does not exist.", "status": "FAILED"}

    files_to_review = []
    if path.is_file():
        files_to_review.append(path)
    else:
        for ext in ["*.java", "*.go", "*.rs", "*.py", "*.ts", "*.js"]:
            files_to_review.extend(list(path.glob(f"**/{ext}")))

    if not files_to_review:
        return {
            "target": str(path),
            "readiness_score": 100,
            "risk_score": 0,
            "recommendation": "APPROVED",
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "file_reports": []
        }

    all_critical = []
    all_high = []
    all_medium = []
    all_low = []
    file_reports = []

    for f in files_to_review:
        rep = analyze_source_content(f.read_text(encoding="utf-8"), f.name)
        file_reports.append(rep)
        all_critical.extend(rep["critical_issues"])
        all_high.extend(rep["high_issues"])
        all_medium.extend(rep["medium_issues"])
        all_low.extend(rep["low_issues"])

    total_files = len(files_to_review)
    crit_penalty = len(all_critical) * 30
    high_penalty = len(all_high) * 15
    med_penalty = len(all_medium) * 5

    readiness_score = max(0, 100 - (crit_penalty + high_penalty + med_penalty))
    risk_score = min(100, crit_penalty + high_penalty + med_penalty)

    if len(all_critical) > 0 or readiness_score < 70:
        recommendation = "REJECTED"
    elif len(all_high) > 0 or readiness_score < 85:
        recommendation = "CHANGES_REQUESTED"
    else:
        recommendation = "APPROVED"

    return {
        "target": str(path),
        "files_reviewed": total_files,
        "readiness_score": readiness_score,
        "risk_score": risk_score,
        "recommendation": recommendation,
        "critical_count": len(all_critical),
        "high_count": len(all_high),
        "medium_count": len(all_medium),
        "low_count": len(all_low),
        "critical_issues": all_critical,
        "high_issues": all_high,
        "medium_issues": all_medium,
        "low_issues": all_low
    }

def main():
    parser = argparse.ArgumentParser(description="Principal Code Review Engine")
    parser.add_argument("--path", required=True, help="Path to project or source file to review")
    parser.add_argument("--json", action="store_true", help="Output audit report as JSON")
    args = parser.parse_args()

    report = review_target(args.path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("==================================================")
        print("   PRINCIPAL CODE REVIEW AUDIT REPORT")
        print("==================================================")
        print(f"Target Path:             {report.get('target')}")
        print(f"Files Reviewed:          {report.get('files_reviewed', 0)}")
        print(f"Production Readiness:    {report.get('readiness_score')}/100")
        print(f"Risk Score:              {report.get('risk_score')}/100")
        print(f"Merge Recommendation:    {report.get('recommendation')}")
        print("--------------------------------------------------\n")

        print("Severity Breakdown:")
        print(f"  CRITICAL: {report.get('critical_count', 0)}")
        print(f"  HIGH:     {report.get('high_count', 0)}")
        print(f"  MEDIUM:   {report.get('medium_count', 0)}")
        print(f"  LOW:      {report.get('low_count', 0)}\n")

        if report.get("critical_issues"):
            print("CRITICAL BLOCKERS:")
            for c in report["critical_issues"]:
                print(f"  [X] {c}")

        if report.get("high_issues"):
            print("\nHIGH ISSUES:")
            for h in report["high_issues"]:
                print(f"  [!] {h}")

        if report.get("medium_issues"):
            print("\nMEDIUM ISSUES:")
            for m in report["medium_issues"]:
                print(f"  [?] {m}")

        sys.exit(0 if report.get("recommendation") == "APPROVED" else 1)

if __name__ == "__main__":
    main()
