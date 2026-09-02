import pytest
from prolog_agent_toolkit.runner import parse_memory_bytes, parse_timeout_seconds, resolve_engine_binary


def test_parse_memory_bytes():
    assert parse_memory_bytes("50M") == 50 * 1024 * 1024
    assert parse_memory_bytes("500K") == 500 * 1024
    assert parse_memory_bytes("1G") == 1 * 1024 * 1024 * 1024
    assert parse_memory_bytes("1000") == 1000
    assert parse_memory_bytes(None) is None


def test_parse_timeout_seconds():
    assert parse_timeout_seconds("20s") == 20.0
    assert parse_timeout_seconds("2m") == 120.0
    assert parse_timeout_seconds("10") == 10.0
    assert parse_timeout_seconds(None) == 20.0


def test_resolve_engine_binary():
    assert resolve_engine_binary("scryer") == "scryer-prolog"
    assert resolve_engine_binary("swi") == "swipl"
    assert resolve_engine_binary("trealla") == "tpl"
    assert resolve_engine_binary("tau") == "tau-prolog"
    assert resolve_engine_binary("gnu") == "gprolog"
    assert resolve_engine_binary("custom-bin") == "custom-bin"


def test_next_fibonacci_increment():
    from prolog_agent_toolkit.runner import next_fibonacci_increment
    p1, n1 = next_fibonacci_increment(3, 5)
    assert (p1, n1) == (5, 8)
    p2, n2 = next_fibonacci_increment(p1, n1)
    assert (p2, n2) == (8, 13)
    p3, n3 = next_fibonacci_increment(p2, n2)
    assert (p3, n3) == (13, 21)
    p4, n4 = next_fibonacci_increment(p3, n3)
    assert (p4, n4) == (21, 34)


def test_is_interactive_toplevel():
    from prolog_agent_toolkit.runner import is_interactive_toplevel
    assert is_interactive_toplevel(["-g", "halt"]) is False
    assert is_interactive_toplevel(["-g", "test, halt."]) is False
    assert is_interactive_toplevel(["-t", "halt"]) is False
