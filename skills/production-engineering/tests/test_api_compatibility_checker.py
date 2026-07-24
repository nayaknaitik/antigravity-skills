"""
Unit tests for api_compatibility_checker.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.api_compatibility_checker import check_compatibility

def test_api_compatibility():
    old_p = SKILL_DIR / "templates" / "03_opentelemetry_observability_schema.json.template"
    new_p = SKILL_DIR / "templates" / "03_opentelemetry_observability_schema.json.template"
    res = check_compatibility(str(old_p), str(new_p))
    assert res["valid"] is True

if __name__ == "__main__":
    test_api_compatibility()
    print("✓ test_api_compatibility passed!")
