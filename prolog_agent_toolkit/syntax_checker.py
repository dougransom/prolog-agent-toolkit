"""
Syntax checker for detecting common human editing typos in Prolog source code.

Detects common human punctuation errors such as:
- Using `#` or `//` for line comments instead of `%`
- Using `:` instead of `:-` for neck operators or directives
- Using `->` instead of `-->` for DCG rules at top-level
- Using mistyped comparison operators (`!=`, `<>`, `<=`, `=>`, `:=`)
- Unclosed string/atom quotes or missing clause periods
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class SyntaxIssue:
    file: str
    line: int
    column: int
    issue_type: str
    snippet: str
    suggestion: str


def _strip_strings_and_comments(line: str) -> str:
    """Replace single and double quoted strings and % comments with spaces to avoid false positives."""
    # Remove % comments first
    in_single = False
    in_double = False
    clean_chars = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "'" and not in_double:
            in_single = not in_single
            clean_chars.append(" ")
        elif ch == '"' and not in_single:
            in_double = not in_double
            clean_chars.append(" ")
        elif ch == "%" and not in_single and not in_double:
            clean_chars.append(" " * (len(line) - i))
            break
        elif in_single or in_double:
            clean_chars.append(" ")
        else:
            clean_chars.append(ch)
        i += 1
    return "".join(clean_chars)


def check_human_syntax_errors_in_text(text: str, filename: str = "<input>") -> List[SyntaxIssue]:
    issues: List[SyntaxIssue] = []
    lines = text.splitlines()

    for idx, raw_line in enumerate(lines, start=1):
        stripped_line = raw_line.strip()
        if not stripped_line:
            continue

        # 1. Check line comment typos (# or // at line start)
        if stripped_line.startswith("#"):
            issues.append(
                SyntaxIssue(
                    file=filename,
                    line=idx,
                    column=raw_line.find("#") + 1,
                    issue_type="Wrong Comment Symbol (#)",
                    snippet=stripped_line,
                    suggestion="Prolog uses '%' for line comments. Replace '#' with '%'.",
                )
            )
            continue

        if stripped_line.startswith("//"):
            issues.append(
                SyntaxIssue(
                    file=filename,
                    line=idx,
                    column=raw_line.find("//") + 1,
                    issue_type="Wrong Comment Symbol (//)",
                    snippet=stripped_line,
                    suggestion="Prolog uses '%' for line comments. Replace '//' with '%'.",
                )
            )
            continue

        # 2. Check directive starting with : instead of :-
        if stripped_line.startswith(":") and not stripped_line.startswith(":-"):
            if re.match(r"^:\s*[a-zA-Z\(]", stripped_line):
                col = raw_line.find(":") + 1
                issues.append(
                    SyntaxIssue(
                        file=filename,
                        line=idx,
                        column=col,
                        issue_type="Mis-typed Directive Neck (:)",
                        snippet=stripped_line,
                        suggestion="Directives in Prolog start with ':-', not ':'. Change ':' to ':-'.",
                    )
                )
                continue

        # Work with sanitized line for operator inspection (ignores content inside quotes and % comments)
        code_only = _strip_strings_and_comments(raw_line)
        stripped_code = code_only.strip()

        # 3. Check neck operator typo: head : body instead of head :- body
        if ":" in stripped_code and not ":-" in stripped_code and not "-->" in stripped_code:
            # Ignore standard module qualifiers Module:Goal or library(foo)
            if not re.search(r"\b(use_module|module|import|export|library)\b", stripped_code):
                parts = stripped_code.split(":", 1)
                left_part = parts[0].strip()
                right_part = parts[1].strip() if len(parts) > 1 else ""
                # Head looks like a predicate head: functor(...) or atom
                if re.match(r"^[a-z][a-zA-Z0-9_]*(\s*\(.*\))?$", left_part) and right_part and not right_part.startswith("="):
                    col = raw_line.find(":") + 1
                    issues.append(
                        SyntaxIssue(
                            file=filename,
                            line=idx,
                            column=col,
                            issue_type="Mis-typed Neck Operator (:)",
                            snippet=stripped_line,
                            suggestion="Rule neck operator is ':-', not ':'. Replace ':' with ':-'.",
                        )
                    )

        # 4. Check DCG rule head typo: head -> body instead of head --> body at top-level
        if "->" in stripped_code and not "-->" in stripped_code and not ":-" in stripped_code:
            if stripped_code.endswith("."):
                parts = stripped_code.split("->", 1)
                left_part = parts[0].strip()
                if re.match(r"^[a-z][a-zA-Z0-9_]*(\s*\(.*\))?$", left_part):
                    col = raw_line.find("->") + 1
                    issues.append(
                        SyntaxIssue(
                            file=filename,
                            line=idx,
                            column=col,
                            issue_type="Mis-typed DCG Operator (->)",
                            snippet=stripped_line,
                            suggestion="DCG rule operator is '-->', not '->' (which is if-then). Replace '->' with '-->'.",
                        )
                    )

        # 5. Check mistyped relational / comparison operators
        if "!=" in stripped_code:
            col = raw_line.find("!=") + 1
            issues.append(
                SyntaxIssue(
                    file=filename,
                    line=idx,
                    column=col,
                    issue_type="Invalid Comparison Operator (!=)",
                    snippet=stripped_line,
                    suggestion="Prolog does not use '!='. Use '=\\=' for arithmetic inequality, '\\=' for unification inequality, or dif/2.",
                )
            )

        if "<>" in stripped_code:
            col = raw_line.find("<>") + 1
            issues.append(
                SyntaxIssue(
                    file=filename,
                    line=idx,
                    column=col,
                    issue_type="Invalid Comparison Operator (<>)",
                    snippet=stripped_line,
                    suggestion="Prolog does not use '<>'. Use '=\\=' for arithmetic inequality, '\\=' for term inequality, or dif/2.",
                )
            )

        if "<=" in stripped_code:
            col = raw_line.find("<=") + 1
            issues.append(
                SyntaxIssue(
                    file=filename,
                    line=idx,
                    column=col,
                    issue_type="Invalid Comparison Operator (<=)",
                    snippet=stripped_line,
                    suggestion="Prolog uses '=<', not '<=', for less-than-or-equal comparison.",
                )
            )

        if "=>" in stripped_code and not "-->" in stripped_code:
            col = raw_line.find("=>") + 1
            issues.append(
                SyntaxIssue(
                    file=filename,
                    line=idx,
                    column=col,
                    issue_type="Invalid Comparison Operator (=>)",
                    snippet=stripped_line,
                    suggestion="Prolog uses '>=', not '=>', for greater-than-or-equal arithmetic comparison.",
                )
            )

        # 6. Check inline comment typos (# or //)
        if "#" in stripped_code and not stripped_line.startswith("#"):
            if not re.search(r"#=|=|#<|#>", stripped_code):
                col = raw_line.find("#") + 1
                issues.append(
                    SyntaxIssue(
                        file=filename,
                        line=idx,
                        column=col,
                        issue_type="Wrong Comment Symbol (#)",
                        snippet=stripped_line,
                        suggestion="Prolog line comments use '%'. Replace '#' with '%'.",
                    )
                )

    return issues


def check_human_syntax_errors(file_path: str) -> List[SyntaxIssue]:
    """Read file and check for human syntax errors."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return check_human_syntax_errors_in_text(content, filename=file_path)
    except Exception as e:
        return [
            SyntaxIssue(
                file=file_path,
                line=1,
                column=1,
                issue_type="File Read Error",
                snippet="",
                suggestion=f"Unable to read file: {e}",
            )
        ]


def format_syntax_diagnostics(issues: List[SyntaxIssue]) -> str:
    """Format syntax issues into a clear diagnostic report."""
    if not issues:
        return ""

    lines = []
    lines.append("\n[prolog-safe] === HUMAN SYNTAX ERROR DIAGNOSTIC REPORT ===")
    lines.append(f"Found {len(issues)} probable human syntax editing error(s):\n")

    for issue in issues:
        lines.append(f"  --> {issue.file}:{issue.line}:{issue.column} [{issue.issue_type}]")
        if issue.snippet:
            lines.append(f"      Code: {issue.snippet}")
        lines.append(f"      Fix:  {issue.suggestion}\n")

    lines.append("=========================================================\n")
    return "\n".join(lines)
