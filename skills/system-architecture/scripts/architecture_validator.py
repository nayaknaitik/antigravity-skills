#!/usr/bin/env python3
"""
System Architecture Validator Engine
Audits High-Level Design (HLD) and Low-Level Design (LLD) documents against
organizational quality standards, architectural principles, security guidelines, and required sections.
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path

REQUIRED_HLD_SECTIONS = [
    "Executive Summary",
    "System Architecture",
    "Technology Stack",
    "Security",
    "Scalability",
    "Reliability",
    "Observability",
    "Trade-off Analysis",
    "Risk Analysis"
]

REQUIRED_LLD_SECTIONS = [
    "Package",
    "Component",
    "Sequence Diagram",
    "Database",
    "Error Handling",
    "Testing Strategy"
]

ARCHITECTURAL_PRINCIPLES = [
    "KISS",
    "YAGNI",
    "SOLID",
    "Separation of Concerns",
    "High Cohesion",
    "Low Coupling"
]

def validate_architecture_doc(doc_path: str) -> dict:
    path = Path(doc_path).resolve()
    if not path.exists() or not path.is_file():
        return {"valid": False, "file": path.name, "errors": [f"File '{doc_path}' not found."], "warnings": [], "checks": []}

    content = path.read_text(encoding="utf-8")
    content_lower = content.lower()
    errors = []
    warnings = []
    checks = []

    # Detect doc type
    is_hld = "high-level design" in content_lower or "hld" in content_lower or "system context" in content_lower
    is_lld = "low-level design" in content_lower or "lld" in content_lower or "package structure" in content_lower

    if is_hld:
        checks.append("Document identified as High-Level Design (HLD)")
        for sec in REQUIRED_HLD_SECTIONS:
            if sec.lower() not in content_lower:
                errors.append(f"HLD missing required section: '{sec}'")
            else:
                checks.append(f"HLD includes section '{sec}'")
    elif is_lld:
        checks.append("Document identified as Low-Level Design (LLD)")
        for sec in REQUIRED_LLD_SECTIONS:
            if sec.lower() not in content_lower:
                errors.append(f"LLD missing required section: '{sec}'")
            else:
                checks.append(f"LLD includes section '{sec}'")
    else:
        warnings.append("Document type ambiguous (neither explicit HLD nor LLD header detected)")

    # Check Mermaid diagram inclusion
    if "```mermaid" not in content:
        warnings.append("Document lacks Mermaid visual architecture diagrams")
    else:
        checks.append("Mermaid visual diagram found")

    # Check Trade-off / Decision rationale
    if "trade-off" not in content_lower and "adr" not in content_lower:
        errors.append("Document lacks Trade-off Analysis or ADR decision rationale")
    else:
        checks.append("Trade-off Analysis / ADR rationale present")

    # Check Security & Observability references
    if "security" not in content_lower and "auth" not in content_lower:
        warnings.append("Document lacks explicit security overview")
    if "observability" not in content_lower and "metrics" not in content_lower:
        warnings.append("Document lacks explicit observability design")

    return {
        "valid": len(errors) == 0,
        "file": path.name,
        "errors": errors,
        "warnings": warnings,
        "passed_checks": checks
    }

def main():
    parser = argparse.ArgumentParser(description="System Architecture Document Validator")
    parser.add_argument("--doc-path", required=True, help="Path to architecture design markdown file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = validate_architecture_doc(args.doc_path)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"=== Architecture Document Audit: {results['file']} ===")
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
