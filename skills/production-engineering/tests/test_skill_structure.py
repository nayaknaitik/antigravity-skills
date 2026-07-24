"""
Unit tests for production-engineering skill structural compliance.
"""

import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

def test_mandatory_directories_exist():
    required = ["references", "assets", "scripts", "templates", "tests", "examples", "metadata", "docs"]
    for folder in required:
        assert (SKILL_DIR / folder).is_dir(), f"Missing required directory: {folder}"

def test_skill_md_exists():
    assert (SKILL_DIR / "SKILL.md").is_file(), "Missing SKILL.md"

def test_metadata_json_exists():
    assert (SKILL_DIR / "metadata" / "skill.json").is_file(), "Missing metadata/skill.json"

def test_docs_exist():
    for doc in ["USER_GUIDE.md", "MAINTAINER_GUIDE.md", "CHANGELOG.md", "INHERITANCE_GUIDE.md"]:
        assert (SKILL_DIR / "docs" / doc).is_file(), f"Missing documentation file: {doc}"
