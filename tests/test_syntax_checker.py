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

from prolog_agent_toolkit.syntax_checker import check_purity_issues_in_text, format_purity_diagnostics


def test_equivalence_operators_no_false_positive():
    code = """
    % Valid reif and constraint operators
    equiv(X, Y) :- X <=> Y.
    impl(X, Y) :- X ==> Y.
    clp_bool(X, Y) :- X #<==> Y, X #==> Y.
    clp_le(X, Y) :- X #<= Y.
    """
    issues = check_human_syntax_errors_in_text(code, "test.pl")
    assert len(issues) == 0


def test_purity_detection_and_justifications():
    code = r"""
    % Unjustified imperative code
    bad1(X, Y) :- X = Y, !.
    bad2(X, Y) :- ( X == Y -> foo ; bar ).
    bad3(X, Y) :- \+ (X = Y).

    % Justified legacy / side-effect code
    good_cut(X) :- write(X), !. % Justification: Interactive prompt side-effect cut
    good_soft(X) :- ( cond -> foo ; bar ). % Justification: Legacy engine compatibility
    pure_ineq(X, Y) :- dif(X, Y).
    """
    issues = check_purity_issues_in_text(code, "test.pl")
    assert len(issues) == 3
    types = [i.issue_type for i in issues]
    assert "Unjustified Non-Logical Cut (!)" in types
    assert "Unjustified Soft Cut (->)" in types
    assert "Negation-as-Failure for Inequality" in types

    report = format_purity_diagnostics(issues)
    assert "DECLARATIVE PURITY AUDIT REPORT" in report
    assert "dif(X, Y)" in report
