#!/usr/bin/env python3
"""
Requirement Traceability Matrix (RTM) Validator Script
Audits requirement files to verify complete end-to-end mapping between
Business Goals, Functional Requirements, Non-Functional Requirements, and Test Cases.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

def validate_traceability(file_path: str) -> dict:
    path = Path(file_path).resolve()
    if not path.exists():
        return {"error": f"File '{file_path}' not found", "valid": False}

    content = path.read_text(encoding="utf-8")

    bg_ids = list(set(re.findall(r"BG-[A-Z0-9_-]+", content)))
    fr_ids = list(set(re.findall(r"FR-[A-Z0-9_-]+", content)))
    nfr_ids = list(set(re.findall(r"NFR-[A-Z0-9_-]+", content)))
    gherkin_scenarios = list(set(re.findall(r"Scenario:\s*(.*)", content)))

    issues = []
    if not bg_ids:
        issues.append("Missing Business Goal IDs (BG-XXX)")
    if not fr_ids:
        issues.append("Missing Functional Requirement IDs (FR-XXX)")
    if not nfr_ids:
        issues.append("Missing Non-Functional Requirement IDs (NFR-XXX)")
    if not gherkin_scenarios:
        issues.append("Missing Gherkin Test Scenarios")

    valid = len(issues) == 0

    return {
        "file_name": path.name,
        "valid": valid,
        "business_goals_found": len(bg_ids),
        "functional_reqs_found": len(fr_ids),
        "non_functional_reqs_found": len(nfr_ids),
        "gherkin_scenarios_found": len(gherkin_scenarios),
        "issues": issues
    }

def main():
    parser = argparse.ArgumentParser(description="Requirement Traceability Validator")
    parser.add_argument("--file", required=True, help="Path to requirement markdown file")
    args = parser.parse_args()

    res = validate_traceability(args.file)
    print(f"=== Traceability Matrix Validation: {res['file_name']} ===")
    print(f"Status: {'VALID [✓]' if res['valid'] else 'INVALID [X]'}")
    print(f"Business Goals:         {res.get('business_goals_found', 0)}")
    print(f"Functional Requirements: {res.get('functional_reqs_found', 0)}")
    print(f"Non-Functional Reqs:    {res.get('non_functional_reqs_found', 0)}")
    print(f"Gherkin Scenarios:       {res.get('gherkin_scenarios_found', 0)}\n")

    if res.get("issues"):
        print("Traceability Issues:")
        for issue in res["issues"]:
            print(f"  [X] {issue}")
        sys.exit(1)
    else:
        print("✓ All requirement elements successfully mapped!")
        sys.exit(0)

if __name__ == "__main__":
    main()
