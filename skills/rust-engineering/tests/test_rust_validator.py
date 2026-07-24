#!/usr/bin/env python3
"""
Unit tests for the Rust Code Validator script.
"""

import os
import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from rust_code_validator import validate_rust_file

class TestRustValidator(unittest.TestCase):
    
    def test_validate_nonexistent_file(self):
        result = validate_rust_file("nonexistent.rs")
        self.assertFalse(result["valid"])

    def test_validate_axum_template(self):
        axum_path = Path(__file__).parent.parent / "templates" / "axum_server_template.rs"
        if axum_path.exists():
            result = validate_rust_file(str(axum_path))
            self.assertTrue(result["valid"], f"Axum template validation failed: {result.get('errors')}")

    def test_validate_tokio_example(self):
        example_path = Path(__file__).parent.parent / "examples" / "tokio_cancellation_shutdown.rs"
        if example_path.exists():
            result = validate_rust_file(str(example_path))
            self.assertTrue(result["valid"], f"Tokio example validation failed: {result.get('errors')}")

if __name__ == "__main__":
    unittest.main()
