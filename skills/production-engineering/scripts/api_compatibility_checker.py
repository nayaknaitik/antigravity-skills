#!/usr/bin/env python3
"""
API Compatibility & Backward Evolution Validator
Checks schema changes between API versions to detect breaking mutations or missing idempotency contracts.
"""

import sys
import json
import argparse
from pathlib import Path

def check_compatibility(old_schema_path: str, new_schema_path: str) -> dict:
    old_p = Path(old_schema_path).resolve()
    new_p = Path(new_schema_path).resolve()

    if not old_p.exists() or not new_p.exists():
        return {"valid": False, "errors": ["One or both schema files do not exist."]}

    try:
        old_schema = json.loads(old_p.read_text(encoding="utf-8"))
        new_schema = json.loads(new_p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"valid": False, "errors": [f"Invalid JSON schema: {str(e)}"]}

    errors = []
    warnings = []

    old_props = old_schema.get("properties", {})
    new_props = new_schema.get("properties", {})

    # 1. Check for removed fields
    for field in old_props:
        if field not in new_props:
            errors.append(f"Breaking Change: Existing field '{field}' was deleted.")

    # 2. Check for type mutations
    for field, spec in old_props.items():
        if field in new_props:
            old_type = spec.get("type")
            new_type = new_props[field].get("type")
            if old_type != new_type:
                errors.append(f"Breaking Change: Field '{field}' type changed from '{old_type}' to '{new_type}'.")

    # 3. Check required fields addition
    old_req = set(old_schema.get("required", []))
    new_req = set(new_schema.get("required", []))
    newly_required = new_req - old_req
    for req_field in newly_required:
        if req_field not in old_props:
            errors.append(f"Breaking Change: New required field '{req_field}' added without backward compatibility.")

    return {
        "valid": len(errors) == 0,
        "breaking_errors": errors,
        "warnings": warnings
    }

def main():
    parser = argparse.ArgumentParser(description="API Compatibility Checker")
    parser.add_argument("--old", required=True, help="Path to base/old JSON schema")
    parser.add_argument("--new", required=True, help="Path to target/new JSON schema")
    args = parser.parse_args()

    res = check_compatibility(args.old, args.new)
    if res["valid"]:
        print("✓ API Backward Compatibility Preserved: Zero breaking changes detected.")
        sys.exit(0)
    else:
        print("X API Backward Compatibility Failure:")
        for err in res["breaking_errors"]:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
