#!/usr/bin/env python3
"""
Unit Test Suite for Skill Architect Validator & Quality Scorer Scripts
"""

import unittest
import os
import sys
import tempfile
import json
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from skill_validator import validate_skill
from quality_scorer import evaluate_skill
from skill_generator import generate_skill

class TestSkillArchitectScripts(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_skill_generation_and_validation(self):
        """Tests that generated skills pass both validation and quality scoring."""
        skill_dir = generate_skill(
            name="test-demo-skill",
            description="A test skill for automated testing suite",
            output_dir=self.output_path
        )
        
        val_result = validate_skill(skill_dir)
        self.assertTrue(val_result["valid"], f"Validation failed with errors: {val_result.get('errors')}")

        score_result = evaluate_skill(skill_dir)
        self.assertGreaterEqual(score_result["total_score"], 85, f"Score below threshold: {score_result['total_score']}")
        self.assertIn(score_result["grade"], ["A", "A+"])

if __name__ == "__main__":
    unittest.main()
