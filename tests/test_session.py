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
