import pytest
from prolog_agent_toolkit.syntax_checker import check_human_syntax_errors_in_text, format_syntax_diagnostics


def test_hash_comment_detection():
    code = """
    # This is a python-style comment
    parent(john, mary).
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 1
    assert issues[0].issue_type == "Wrong Comment Symbol (#)"
    assert issues[0].line == 2


def test_slash_comment_detection():
    code = """
    // This is a C-style comment
    parent(john, mary).
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 1
    assert issues[0].issue_type == "Wrong Comment Symbol (//)"
    assert issues[0].line == 2


def test_colon_neck_operator_detection():
    code = """
    father(X, Y) : parent(X, Y), male(X).
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 1
    assert issues[0].issue_type == "Mis-typed Neck Operator (:)"
    assert issues[0].line == 2


def test_colon_directive_detection():
    code = """
    : use_module(library(dcgs)).
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 1
    assert issues[0].issue_type == "Mis-typed Directive Neck (:)"
    assert issues[0].line == 2


def test_dcg_arrow_detection():
    code = """
    sentence -> noun_phrase, verb_phrase.
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 1
    assert issues[0].issue_type == "Mis-typed DCG Operator (->)"
    assert issues[0].line == 2


def test_invalid_comparison_operators():
    code = """
    check_val(X, Y) :- X != Y, X <= Y, X => Y.
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 3
    types = [i.issue_type for i in issues]
    assert "Invalid Comparison Operator (!=)" in types
    assert "Invalid Comparison Operator (<=)" in types
    assert "Invalid Comparison Operator (=>)" in types


def test_clean_prolog_code():
    code = """
    :- use_module(library(dcgs)).

    % Valid prolog comment
    father(X, Y) :-
        parent(X, Y),
        male(X).

    noun_phrase --> noun.

    is_equal(X, Y) :-
        if_(X = Y, true, false).
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 0


def test_format_syntax_diagnostics():
    code = "# comment typo\nfoo : bar."
    issues = check_human_syntax_errors_in_text(code, "sample.pl")
    report = format_syntax_diagnostics(issues)
    assert "HUMAN SYNTAX ERROR DIAGNOSTIC REPORT" in report
    assert "sample.pl:1" in report
    assert "sample.pl:2" in report
