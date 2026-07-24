#!/usr/bin/env python3
"""
Unit tests for the System Architecture Validator engine.
"""

import os
import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from architecture_validator import validate_architecture_doc

class TestArchitectureValidator(unittest.TestCase):
    
    def test_validate_nonexistent_file(self):
        result = validate_architecture_doc("nonexistent_hld.md")
        self.assertFalse(result["valid"])
        self.assertIn("File 'nonexistent_hld.md' not found.", result["errors"][0])

    def test_validate_hld_example(self):
        hld_path = Path(__file__).parent.parent / "examples" / "trading_platform_hld.md"
        if hld_path.exists():
            result = validate_architecture_doc(str(hld_path))
            self.assertTrue(result["valid"], f"HLD validation failed: {result.get('errors')}")

    def test_validate_lld_example(self):
        lld_path = Path(__file__).parent.parent / "examples" / "order_management_system_lld.md"
        if lld_path.exists():
            result = validate_architecture_doc(str(lld_path))
            self.assertTrue(result["valid"], f"LLD validation failed: {result.get('errors')}")

if __name__ == "__main__":
    unittest.main()
