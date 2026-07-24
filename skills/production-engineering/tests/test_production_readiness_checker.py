"""
Unit tests for production_readiness_checker.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.production_readiness_checker import audit_blueprint

def test_audit_golden_example():
    spec_path = SKILL_DIR / "examples" / "01_production_payment_service_spec.json"
    result = audit_blueprint(str(spec_path))
    assert result["score"] >= 85
    assert result["status"] == "APPROVED"

def test_audit_missing_file():
    result = audit_blueprint(str(SKILL_DIR / "non_existent.yaml"))
    assert result["status"] == "FAILED"

if __name__ == "__main__":
    test_audit_golden_example()
    test_audit_missing_file()
    print("✓ test_production_readiness_checker passed!")
