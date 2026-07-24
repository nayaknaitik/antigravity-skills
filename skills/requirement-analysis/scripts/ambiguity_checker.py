#!/usr/bin/env python3
"""
Requirement Ambiguity & Quality Audit Engine
Scans requirement markdown files for ambiguous, unquantified terms, missing metrics,
and missing Gherkin acceptance criteria scenarios.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

VAGUE_TERMS = [
    r"\bfast\b",
    r"\breal-time\b",
    r"\brealtime\b",
    r"\bscalable\b",
    r"\bhigh availability\b",
    r"\buser-friendly\b",
    r"\brobust\b",
    r"\bfault-tolerant\b",
    r"\blow latency\b",
    r"\bultra-low latency\b",
    r"\bhigh throughput\b",
    r"\bsecure\b",
    r"\befficient\b",
    r"\bseamless\b"
]

def audit_requirements_file(file_path: str) -> dict:
    path = Path(file_path).resolve()
    if not path.exists() or not path.is_file():
        return {"error": f"File '{file_path}' not found", "ambiguities_found": [], "score": 0}

    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    ambiguities = []
    
    # 1. Scan for unquantified vague terms
    for line_idx, line in enumerate(lines, 1):
        for term_pattern in VAGUE_TERMS:
            match = re.search(term_pattern, line, re.IGNORECASE)
            if match:
                # Check if numerical metric exists on same line or adjacent lines
                has_metric = bool(re.search(r"\d+(\.\d+)?\s*(ms|µs|us|s|sec|msg/s|tps|%|clicks|USD|mb|gb)", line, re.IGNORECASE))
                if not has_metric:
                    ambiguities.append({
                        "line": line_idx,
                        "term": match.group(0),
                        "snippet": line.strip(),
                        "reason": f"Vague term '{match.group(0)}' used without explicit quantitative metric threshold."
                    })

    # 2. Scan for Gherkin Acceptance Criteria
    has_gherkin = "Scenario:" in content and "Given" in content and "When" in content and "Then" in content
    
    # 3. Scan for Functional Requirements IDs
    fr_ids = re.findall(r"FR-[A-Z0-9_-]+", content)

    score = 100 - (len(ambiguities) * 5)
    if not has_gherkin:
        score -= 20
    score = max(0, score)

    return {
        "file_name": path.name,
        "total_lines": len(lines),
        "ambiguities_found": ambiguities,
        "has_gherkin_acceptance_criteria": has_gherkin,
        "functional_requirements_count": len(set(fr_ids)),
        "quality_score": score,
        "passed": score >= 80 and len(ambiguities) == 0
    }

def main():
    parser = argparse.ArgumentParser(description="Requirement Ambiguity Audit Engine")
    parser.add_argument("--file", required=True, help="Path to requirement markdown file")
    parser.add_argument("--json", action="store_true", help="Output report in JSON format")
    args = parser.parse_args()

    report = audit_requirements_file(args.file)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"=== Requirement Ambiguity Report: {report['file_name']} ===")
        print(f"Quality Score: {report['quality_score']}/100")
        print(f"Status:        {'PASSED' if report['passed'] else 'REJECTED (Contains Ambiguity)'}")
        print(f"Gherkin Criteria: {'Found [✓]' if report['has_gherkin_acceptance_criteria'] else 'Missing [X]'}\n")

        if report["ambiguities_found"]:
            print("Detected Ambiguous / Unquantified Terms:")
            for amb in report["ambiguities_found"]:
                print(f"  Line {amb['line']:3d}: Term '{amb['term']}' -> {amb['reason']}")
                print(f"            Snippet: \"{amb['snippet']}\"\n")
        else:
            print("✓ Zero unquantified vague terms detected!")

        sys.exit(0 if report['passed'] else 1)

if __name__ == "__main__":
    main()
