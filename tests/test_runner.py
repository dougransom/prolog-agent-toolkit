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
    assert resolve_engine_binary("gnu") == "gprolog"
    assert resolve_engine_binary("custom-bin") == "custom-bin"
