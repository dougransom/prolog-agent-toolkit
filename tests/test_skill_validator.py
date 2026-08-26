import os
import tempfile
import pytest
from prolog_agent_toolkit.skill_validator import (
    parse_yaml_frontmatter,
    validate_skill_file,
    validate_skills_dir,
    format_skill_issues,
)


def test_parse_yaml_frontmatter_valid():
    content = """---
name: prolog-testing
description: Standardized instructions for testing
---
# Body
Some instructions
"""
    fm = parse_yaml_frontmatter(content)
    assert fm is not None
    assert fm["name"] == "prolog-testing"
    assert fm["description"] == "Standardized instructions for testing"


def test_parse_yaml_frontmatter_invalid():
    content = "# Just markdown without frontmatter"
    fm = parse_yaml_frontmatter(content)
    assert fm is None


def test_validate_skill_file_missing_keys():
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = os.path.join(tmpdir, "my-skill")
        os.makedirs(skill_dir)
        skill_file = os.path.join(skill_dir, "SKILL.md")

        # Missing description
        with open(skill_file, "w") as f:
            f.write("---\nname: test-skill\n---\nBody")

        issues = validate_skill_file(skill_file)
        assert len(issues) == 1
        assert issues[0].issue_type == "Missing Frontmatter Key"
        assert "description" in issues[0].message


def test_validate_skill_file_exceeds_max_lines():
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = os.path.join(tmpdir, "large-skill")
        os.makedirs(skill_dir)
        skill_file = os.path.join(skill_dir, "SKILL.md")

        lines = ["---\nname: large\ndescription: large skill\n---\n"] + ["line\n"] * 600
        with open(skill_file, "w") as f:
            f.writelines(lines)

        issues = validate_skill_file(skill_file, max_lines=500)
        assert len(issues) == 1
        assert issues[0].issue_type == "Line Limit Exceeded"


def test_validate_skills_dir_real_skills():
    # Test running against repository's own .agents/skills directory
    skills_path = ".agents/skills"
    if os.path.exists(skills_path):
        issues = validate_skills_dir(skills_path)
        # Should pass without fatal frontmatter missing issues
        fatal_issues = [i for i in issues if i.issue_type == "Missing Frontmatter"]
        assert len(fatal_issues) == 0
