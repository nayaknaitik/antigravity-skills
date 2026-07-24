"""
Unit tests for java-engineering skill structure compliance.
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

def test_mandatory_directories():
    folders = ["references", "assets", "scripts", "templates", "tests", "examples", "metadata", "docs"]
    for folder in folders:
        assert (SKILL_DIR / folder).is_dir(), f"Missing required directory: {folder}"

def test_skill_md_and_metadata():
    assert (SKILL_DIR / "SKILL.md").is_file()
    assert (SKILL_DIR / "metadata" / "skill.json").is_file()

def test_docs_exist():
    for doc in ["USER_GUIDE.md", "MAINTAINER_GUIDE.md", "CHANGELOG.md", "SPRING_BOOT_3_GUIDE.md"]:
        assert (SKILL_DIR / "docs" / doc).is_file(), f"Missing doc: {doc}"

if __name__ == "__main__":
    test_mandatory_directories()
    test_skill_md_and_metadata()
    test_docs_exist()
    print("✓ test_skill_structure passed!")
