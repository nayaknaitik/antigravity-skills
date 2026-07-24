"""
Unit tests for java_code_linter.py
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.java_code_linter import audit_project

def test_linter_on_examples():
    examples_dir = SKILL_DIR / "examples"
    res = audit_project(str(examples_dir))
    assert res["status"] == "APPROVED"
    assert res["score"] >= 85

if __name__ == "__main__":
    test_linter_on_examples()
    print("✓ test_java_linter passed!")
