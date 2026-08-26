import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SkillIssue:
    skill_name: str
    file_path: str
    issue_type: str
    message: str
    line: Optional[int] = None

    def __str__(self) -> str:
        loc = f"{self.file_path}:{self.line}" if self.line else self.file_path
        return f"[{self.issue_type}] {loc} - {self.message}"


def parse_yaml_frontmatter(content: str) -> Optional[dict]:
    """Extract and parse basic YAML frontmatter from SKILL.md content without external deps."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None

    yaml_block = match.group(1)
    data = {}
    for line in yaml_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip().strip('"').strip("'")
            data[key] = val
    return data


def validate_skill_file(file_path: str, max_lines: int = 500) -> List[SkillIssue]:
    """Validate a single SKILL.md file for frontmatter, line limits, and broken markdown links."""
    issues = []
    skill_name = os.path.basename(os.path.dirname(file_path))

    if not os.path.exists(file_path):
        issues.append(
            SkillIssue(
                skill_name=skill_name,
                file_path=file_path,
                issue_type="Missing File",
                message="SKILL.md file does not exist.",
            )
        )
        return issues

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        issues.append(
            SkillIssue(
                skill_name=skill_name,
                file_path=file_path,
                issue_type="Read Error",
                message=f"Could not read file: {e}",
            )
        )
        return issues

    lines = content.splitlines()

    # 1. Line count check
    if len(lines) > max_lines:
        issues.append(
            SkillIssue(
                skill_name=skill_name,
                file_path=file_path,
                issue_type="Line Limit Exceeded",
                message=f"File contains {len(lines)} lines, exceeding recommended limit of {max_lines} lines.",
            )
        )

    # 2. YAML frontmatter check
    frontmatter = parse_yaml_frontmatter(content)
    if frontmatter is None:
        issues.append(
            SkillIssue(
                skill_name=skill_name,
                file_path=file_path,
                issue_type="Missing Frontmatter",
                message="File missing valid '---' YAML frontmatter header.",
                line=1,
            )
        )
    else:
        if "name" not in frontmatter or not frontmatter["name"]:
            issues.append(
                SkillIssue(
                    skill_name=skill_name,
                    file_path=file_path,
                    issue_type="Missing Frontmatter Key",
                    message="YAML frontmatter missing required 'name' field.",
                    line=1,
                )
            )
        if "description" not in frontmatter or not frontmatter["description"]:
            issues.append(
                SkillIssue(
                    skill_name=skill_name,
                    file_path=file_path,
                    issue_type="Missing Frontmatter Key",
                    message="YAML frontmatter missing required 'description' field.",
                    line=1,
                )
            )

    return issues


def validate_skills_dir(skills_dir: str, max_lines: int = 500) -> List[SkillIssue]:
    """Recursively validate all skills inside a directory."""
    all_issues = []
    if not os.path.exists(skills_dir):
        all_issues.append(
            SkillIssue(
                skill_name=os.path.basename(skills_dir),
                file_path=skills_dir,
                issue_type="Directory Not Found",
                message=f"Skills directory '{skills_dir}' does not exist.",
            )
        )
        return all_issues

    for root, dirs, files in os.walk(skills_dir):
        # A skill directory contains SKILL.md
        if "SKILL.md" in files:
            skill_md_path = os.path.join(root, "SKILL.md")
            issues = validate_skill_file(skill_md_path, max_lines=max_lines)
            all_issues.extend(issues)

    return all_issues


def format_skill_issues(issues: List[SkillIssue]) -> str:
    """Format a list of SkillIssues into a diagnostic report."""
    if not issues:
        return "[prolog-validate-skills] All skills validated successfully. No issues found.\n"

    lines = ["==================================================================", "SKILL VALIDATION DIAGNOSTIC REPORT", "=================================================================="]
    for issue in issues:
        lines.append(str(issue))
    lines.append(f"\nTotal Issues Found: {len(issues)}")
    return "\n".join(lines) + "\n"


def validate_skills_cli(target_dir: Optional[str] = None) -> int:
    """CLI handler for prolog-validate-skills command."""
    if target_dir is None:
        args = [a for a in sys.argv[1:] if not a.startswith("-") and a != "validate-skills"]
        target_dir = args[0] if args else ".agents/skills"

    issues = validate_skills_dir(target_dir)
    report = format_skill_issues(issues)


    if issues:
        sys.stderr.write(report)
        return 1
    else:
        sys.stdout.write(report)
        return 0


if __name__ == "__main__":
    sys.exit(validate_skills_cli())
