#!/usr/bin/env python3
"""
Rust Engineering Code & Architecture Validator
Audits Rust source files, project structures, and code snippets against
organizational production engineering standards, memory safety rules, and error handling practices.
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path

def validate_rust_file(file_path: str) -> dict:
    path = Path(file_path).resolve()
    if not path.exists() or not path.is_file():
        return {
            "valid": False,
            "file": path.name,
            "errors": [f"File '{file_path}' not found."],
            "warnings": [],
            "passed_checks": []
        }

    content = path.read_text(encoding="utf-8")
    errors = []
    warnings = []
    checks = []

    # 1. Check for unwrap() calls (production risk)
    unwrap_matches = re.findall(r'\.unwrap\(\)', content)
    if len(unwrap_matches) > 0:
        warnings.append(f"Found {len(unwrap_matches)} instance(s) of '.unwrap()' - prefer explicit '?' operator or '.expect(\"rationale\")'")
    else:
        checks.append("No bare '.unwrap()' calls found")

    # 2. Check for unsafe code without SAFETY comment
    unsafe_blocks = re.findall(r'unsafe\s*\{', content)
    safety_comments = re.findall(r'//\s*SAFETY:', content, re.IGNORECASE)

    if len(unsafe_blocks) > 0:
        checks.append(f"Found {len(unsafe_blocks)} unsafe block(s)")
        if len(safety_comments) < len(unsafe_blocks):
            errors.append(f"Found {len(unsafe_blocks)} unsafe block(s) but only {len(safety_comments)} mandatory '// SAFETY:' comment(s)")
        else:
            checks.append("All unsafe blocks are documented with '// SAFETY:' comments")
    else:
        checks.append("No unsafe code blocks found (safe Rust verified)")

    # 3. Check for error handling imports (thiserror / anyhow / std::error::Error)
    if "thiserror" in content or "anyhow" in content or "Result<" in content:
        checks.append("Structured error handling pattern identified")
    else:
        warnings.append("File does not appear to use structured error handling primitives")

    # 4. Check for tracing / logging
    if "tracing::" in content or "log::" in content:
        checks.append("Structured tracing/logging instrumentation found")

    return {
        "valid": len(errors) == 0,
        "file": path.name,
        "errors": errors,
        "warnings": warnings,
        "passed_checks": checks
    }

def main():
    parser = argparse.ArgumentParser(description="Rust Production Code Validator")
    parser.add_argument("--file-path", required=True, help="Path to Rust source (.rs) file to audit")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = validate_rust_file(args.file_path)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"=== Rust Code Quality Audit: {results['file']} ===")
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
