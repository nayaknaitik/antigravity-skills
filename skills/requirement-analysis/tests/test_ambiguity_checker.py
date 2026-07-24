#!/usr/bin/env python3
"""
Unit Test Suite for Requirement Analysis Automated Scripts
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from ambiguity_checker import audit_requirements_file
from traceability_validator import validate_traceability

class TestRequirementAnalysisScripts(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test_req.md"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ambiguity_detection_valid(self):
        content = """# Order Risk Requirement
BG-01: Sub-50-Microsecond Risk Checks
FR-RISK-01: Pre-trade order check
NFR-LAT-01: Risk engine latency MUST be < 50 microseconds (p99).

Feature: Pre-Trade Risk
  Scenario: Order Value Check
    Given a trader account with limit $500,000 USD
    When an order of $750,000 USD is submitted
    Then the system MUST REJECT the order in < 50 microseconds.
"""
        self.test_file.write_text(content, encoding="utf-8")
        
        report = audit_requirements_file(str(self.test_file))
        self.assertTrue(report["passed"], f"Expected pass, got ambiguities: {report['ambiguities_found']}")
        
        trace_report = validate_traceability(str(self.test_file))
        self.assertTrue(trace_report["valid"], f"Expected valid traceability, got issues: {trace_report['issues']}")

    def test_ambiguity_detection_vague_fails(self):
        content = """# Vague Requirement
System needs to be fast and real-time.
"""
        self.test_file.write_text(content, encoding="utf-8")
        
        report = audit_requirements_file(str(self.test_file))
        self.assertFalse(report["passed"])
        self.assertGreater(len(report["ambiguities_found"]), 0)

if __name__ == "__main__":
    unittest.main()
