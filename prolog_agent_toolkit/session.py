import os
import sys
import time
import shutil
import signal
import platform
import subprocess
import select
import uuid
from typing import List, Optional, Union

from prolog_agent_toolkit.runner import (
    resolve_engine_binary,
    parse_timeout_seconds,
    parse_memory_bytes,
    set_process_limits_posix,
    kill_process_tree,
)


class QueryResult:
    """Encapsulates the result of posting a query to a running Prolog top-level."""

    def __init__(
        self,
        query: str,
        output: str,
        timed_out: bool = False,
        execution_time: float = 0.0,
        status: str = "success",
        exit_code: Optional[int] = None,
    ):
        self.query = query
        self.output = output
        self.timed_out = timed_out
        self.execution_time = execution_time
        self.status = status
        self.exit_code = exit_code

    def __repr__(self) -> str:
        return (
            f"QueryResult(query={self.query!r}, status={self.status!r}, "
            f"timed_out={self.timed_out}, execution_time={self.execution_time:.3f}s)"
        )


class PrologSession:
    """Persistent, interactive Prolog top-level session.
    
    Allows software agents to post multiple queries sequentially to a running Prolog interpreter
    while enforcing per-query safety timeouts. The underlying Prolog process remains alive across
    queries and is ONLY terminated if a posted query exceeds the configured timeout.
    """

    def __init__(
        self,
        engine: Optional[str] = None,
        files: Optional[List[str]] = None,
        timeout: Optional[Union[str, float]] = None,
        memory: Optional[str] = None,
        cpu_quota: Optional[str] = None,
    ):
        self.engine_name = engine or os.environ.get("PROLOG_ENGINE", "scryer")
        self.timeout_sec = parse_timeout_seconds(
            str(timeout) if timeout is not None else os.environ.get("PROLOG_TIMEOUT", "20s")
        )
        self.memory_str = memory or os.environ.get("PROLOG_MEMORY_MAX", "500M")

        self.cpu_quota_str = cpu_quota or os.environ.get("PROLOG_CPU_QUOTA", "65%")
        self.files = files or []

        self.engine_bin = resolve_engine_binary(self.engine_name)
        self.bin_path = shutil.which(self.engine_bin)
        if not self.bin_path:
            raise RuntimeError(f"Prolog engine binary '{self.engine_bin}' not found on PATH.")

        self.proc: Optional[subprocess.Popen] = None
        self.master_fd: Optional[int] = None
        self.slave_fd: Optional[int] = None
        self._is_alive = False
        self._system_name = platform.system()

        self._start_session()

        for f in self.files:
            if os.path.exists(f):
                self.consult(f)

    def _start_session(self) -> None:
        """Start the background Prolog process with safe process controls."""
        memory_bytes = parse_memory_bytes(self.memory_str)
        full_cmd = [self.bin_path]

        preexec_fn = None
        if self._system_name != "Windows":
            preexec_fn = lambda: set_process_limits_posix(memory_bytes)

        if self._system_name != "Windows" and hasattr(os, "openpty"):
            import pty
            import termios

            self.master_fd, self.slave_fd = pty.openpty()
            try:
                attrs = termios.tcgetattr(self.slave_fd)
                attrs[3] = attrs[3] & ~termios.ECHO
                termios.tcsetattr(self.slave_fd, termios.TCSANOW, attrs)
            except Exception:
                pass

            self.proc = subprocess.Popen(
                full_cmd,
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                preexec_fn=preexec_fn,
                close_fds=True,
            )
            os.close(self.slave_fd)
            self.slave_fd = None
        else:
            self.proc = subprocess.Popen(
                full_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                preexec_fn=preexec_fn,
            )

        self._is_alive = True
        self._read_flush_initial(timeout=1.0)

    def _read_flush_initial(self, timeout: float = 0.5) -> None:
        """Drain initial startup banner / prompt header."""
        start = time.time()
        while time.time() - start < timeout:
            if self.master_fd is not None:
                r, _, _ = select.select([self.master_fd], [], [], 0.05)
                if r:
                    try:
                        data = os.read(self.master_fd, 1024)
                        if not data:
                            break
                    except OSError:
                        break
                else:
                    break
            elif self.proc and self.proc.stdout:
                r, _, _ = select.select([self.proc.stdout], [], [], 0.05)
                if r:
                    try:
                        data = self.proc.stdout.read(1024)
                        if not data:
                            break
                    except Exception:
                        break
                else:
                    break

    def is_alive(self) -> bool:
        """Check whether the Prolog process session is currently active and running."""
        if not self._is_alive or not self.proc:
            return False
        return self.proc.poll() is None

    def query(self, query_str: str, timeout: Optional[Union[str, float]] = None) -> QueryResult:
        """Post a query to the running Prolog top-level.
        
        Enforces a per-query safety timeout. If the query responds within the timeout, the session
        remains active for future queries. If the query times out (does not respond), the Prolog
        process is terminated immediately.
        """
        if not self.is_alive():
            return QueryResult(
                query=query_str,
                output="[prolog-safe] ERROR: Prolog session is not active.",
                timed_out=False,
                status="error",
                exit_code=1,
            )

        timeout_sec = parse_timeout_seconds(str(timeout)) if timeout is not None else self.timeout_sec

        cleaned_query = query_str.strip()
        if cleaned_query.endswith("."):
            cleaned_term = cleaned_query[:-1].strip()
        else:
            cleaned_term = cleaned_query
            cleaned_query += "."

        sentinel = f"__PROLOG_AGENT_DONE_{uuid.uuid4().hex[:8]}__"
        sentinel_cmd = f"write('{sentinel}'), nl, flush_output."

        if cleaned_query.startswith(":-") or cleaned_query.startswith("consult(") or cleaned_query.startswith("use_module(") or cleaned_query == "halt.":
            payload = f"{cleaned_query}\n{sentinel_cmd}\n"
        else:
            payload = f"once(({cleaned_term})).\n{sentinel_cmd}\n"




        start_time = time.time()

        try:
            if self.master_fd is not None:
                os.write(self.master_fd, payload.encode("utf-8"))
            elif self.proc and self.proc.stdin:
                self.proc.stdin.write(payload)
                self.proc.stdin.flush()
        except Exception as e:
            self._is_alive = False
            return QueryResult(
                query=query_str,
                output=f"[prolog-safe] ERROR: Failed to write to Prolog session: {e}",
                timed_out=False,
                status="error",
                exit_code=1,
            )

        captured = []
        timed_out = False

        while time.time() - start_time < timeout_sec:
            remaining = timeout_sec - (time.time() - start_time)
            if remaining <= 0:
                timed_out = True
                break

            if self.master_fd is not None:
                r, _, _ = select.select([self.master_fd], [], [], min(remaining, 0.1))
                if r:
                    try:
                        data = os.read(self.master_fd, 4096)
                        if not data:
                            break
                        chunk_str = data.decode("utf-8", errors="ignore")
                        captured.append(chunk_str)
                        if sentinel in "".join(captured):
                            break
                    except OSError:
                        break
            elif self.proc and self.proc.stdout:
                r, _, _ = select.select([self.proc.stdout], [], [], min(remaining, 0.1))
                if r:
                    try:
                        chunk = self.proc.stdout.read(4096)
                        if not chunk:
                            break
                        captured.append(chunk if isinstance(chunk, str) else chunk.decode("utf-8", errors="ignore"))
                        if sentinel in "".join(captured):
                            break
                    except Exception:
                        break

        elapsed = time.time() - start_time
        full_output = "".join(captured)
        has_sentinel = sentinel in full_output

        if has_sentinel:
            full_output = full_output.replace(sentinel, "").strip()

        if timed_out or not has_sentinel:
            timed_out = True
            self.terminate()
            err_msg = f"[prolog-safe] ERROR: Posted query timed out after {timeout_sec}s. Terminating Prolog process tree."
            return QueryResult(
                query=query_str,
                output=f"{full_output}\n{err_msg}".strip(),
                timed_out=True,
                execution_time=elapsed,
                status="timeout",
                exit_code=124,
            )

        return QueryResult(
            query=query_str,
            output=full_output,
            timed_out=False,
            execution_time=elapsed,
            status="success",
            exit_code=0,
        )

    def consult(self, file_path: str) -> QueryResult:
        """Consult/load a Prolog file into the running session."""
        abs_path = os.path.abspath(file_path)
        escaped_path = abs_path.replace("'", "\\'")
        goal = f"consult('{escaped_path}')."
        return self.query(goal)

    def terminate(self) -> None:
        """Terminate the running process tree and clean up open descriptors."""
        self._is_alive = False
        if self.proc and self.proc.pid:
            kill_process_tree(self.proc.pid)
            self.proc = None
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None

    def close(self) -> None:
        """Gracefully close the session (sending halt. or terminating)."""
        if self.is_alive():
            try:
                self.query("halt.", timeout=1.0)
            except Exception:
                pass
            self.terminate()

    def __enter__(self) -> "PrologSession":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
