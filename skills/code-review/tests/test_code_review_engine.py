"""
Unit tests for code_review_engine.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.code_review_engine import review_target

def test_flawed_code_rejected():
    flawed_file = SKILL_DIR / "examples" / "flawed_payment_code.java"
    report = review_target(str(flawed_file))
    assert report["recommendation"] == "REJECTED"
    assert report["critical_count"] >= 1

def test_production_code_approved():
    prod_file = SKILL_DIR / "examples" / "production_ready_payment_code.java"
    report = review_target(str(prod_file))
    assert report["recommendation"] == "APPROVED"
    assert report["readiness_score"] >= 85

if __name__ == "__main__":
    test_flawed_code_rejected()
    test_production_code_approved()
    print("✓ test_code_review_engine passed!")
