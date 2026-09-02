import os
import shutil
import tempfile
import pytest
from prolog_agent_toolkit.session import PrologSession, QueryResult


@pytest.fixture
def scryer_engine():
    engine_bin = shutil.which("scryer-prolog")
    if not engine_bin:
        pytest.skip("scryer-prolog binary not found on PATH")
    return "scryer"


def test_session_basic_query(scryer_engine):
    with PrologSession(engine=scryer_engine, timeout="3s") as session:
        assert session.is_alive()
        res = session.query("X = 42.")
        assert isinstance(res, QueryResult)
        assert res.timed_out is False
        assert res.status == "success"
        assert "42" in res.output
        assert session.is_alive()


def test_session_successive_queries_state(scryer_engine):
    with PrologSession(engine=scryer_engine, timeout="3s") as session:
        assert session.is_alive()

        res1 = session.query("X = 10.")
        assert res1.timed_out is False
        assert "10" in res1.output
        assert session.is_alive()

        res2 = session.query("Y = 20, Z is Y * 2.")
        assert res2.timed_out is False
        assert "40" in res2.output
        assert session.is_alive()


def test_session_per_query_timeout(scryer_engine):
    with PrologSession(engine=scryer_engine, timeout="1s") as session:
        assert session.is_alive()

        res1 = session.query("X = 1.")
        assert res1.timed_out is False

        # Post an infinite loop query
        res2 = session.query("repeat, fail.", timeout="1s")
        assert res2.timed_out is True
        assert res2.status == "timeout"
        assert "[prolog-safe] ERROR" in res2.output
        # Verify that process was terminated
        assert session.is_alive() is False


def test_session_consult_file(scryer_engine):
    with tempfile.NamedTemporaryFile("w", suffix=".pl", delete=False) as f:
        f.write("test_fact(123).\n")
        f_path = f.name

    try:
        with PrologSession(engine=scryer_engine, files=[f_path], timeout="3s") as session:
            res = session.query("test_fact(X).")
            assert res.timed_out is False
            assert "123" in res.output
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_session_interactive_prompt_kill(scryer_engine):
    called_with = []

    def mock_prompt(elapsed, next_inc):
        called_with.append((elapsed, next_inc))
        return False  # User declines extension, killing process

    with PrologSession(
        engine=scryer_engine,
        timeout="0.5s",
        interactive=True,
        prompt_callback=mock_prompt,
    ) as session:
        res = session.query("repeat, fail.")
        assert res.timed_out is True
        assert res.status == "cancelled"
        assert "Query terminated by user" in res.output
        assert session.is_alive() is False
        assert len(called_with) == 1
        assert called_with[0][1] == 8  # Next Fibonacci number after 5 is 8


def test_session_interactive_prompt_extend_then_kill(scryer_engine):
    called_with = []

    def mock_prompt(elapsed, next_inc):
        called_with.append((elapsed, next_inc))
        if len(called_with) == 1:
            return True  # User approves 1st extension (8s)
        return False     # User declines 2nd extension (13s)

    with PrologSession(
        engine=scryer_engine,
        timeout="0.4s",
        interactive=True,
        prompt_callback=mock_prompt,
    ) as session:
        # Override initial interval so it suspends quickly for test
        res = session.query("repeat, fail.", timeout="0.4s")
        assert res.timed_out is True
        assert res.status == "cancelled"
        assert len(called_with) >= 2
        # Verify sequence: first prompt proposed 8s, second prompt proposed 13s
        assert called_with[0][1] == 8
        assert called_with[1][1] == 13

