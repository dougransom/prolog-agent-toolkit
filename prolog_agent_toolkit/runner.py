import os
import sys
import time
import shutil
import signal
import platform
import subprocess
from typing import List, Optional

import psutil


def parse_memory_bytes(mem_str: str) -> Optional[int]:
    """Parse human memory limits like '50M', '500K', '1G', '1048576' into bytes."""
    if not mem_str:
        return None
    mem_str = mem_str.strip().upper()
    try:
        if mem_str.endswith("K") or mem_str.endswith("KB"):
            num = float(mem_str.rstrip("K").rstrip("B"))
            return int(num * 1024)
        elif mem_str.endswith("M") or mem_str.endswith("MB"):
            num = float(mem_str.rstrip("M").rstrip("B"))
            return int(num * 1024 * 1024)
        elif mem_str.endswith("G") or mem_str.endswith("GB"):
            num = float(mem_str.rstrip("G").rstrip("B"))
            return int(num * 1024 * 1024 * 1024)
        else:
            return int(mem_str)
    except ValueError:
        return None


def parse_timeout_seconds(timeout_str: str) -> float:
    """Parse timeout strings like '20s', '2m', '10' into seconds float."""
    if not timeout_str:
        return 20.0
    timeout_str = timeout_str.strip().lower()
    try:
        if timeout_str.endswith("s"):
            return float(timeout_str[:-1])
        elif timeout_str.endswith("m"):
            return float(timeout_str[:-1]) * 60.0
        elif timeout_str.endswith("h"):
            return float(timeout_str[:-1]) * 3600.0
        else:
            return float(timeout_str)
    except ValueError:
        return 20.0


def resolve_engine_binary(engine_name: str) -> str:
    """Map engine name/alias to actual system binary name."""
    engine = engine_name.lower().strip()
    mapping = {
        "scryer": "scryer-prolog",
        "scryer-prolog": "scryer-prolog",
        "swi": "swipl",
        "swipl": "swipl",
        "trealla": "tpl",
        "tpl": "tpl",
        "gnu": "gprolog",
        "gprolog": "gprolog",
        "tau": "tau-prolog",
        "tau-prolog": "tau-prolog",
        "ciao": "ciao",
        "sicstus": "sicstus",
    }
    return mapping.get(engine, engine_name)


def set_process_limits_posix(memory_bytes: Optional[int]) -> None:
    """Apply POSIX resource limits (nice priority, RLIMIT_AS)."""
    # Lower CPU priority
    try:
        os.nice(19)
    except Exception:
        pass

    # RLIMIT_AS for memory limit if supported
    if memory_bytes and memory_bytes > 0:
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
        except Exception:
            pass


def kill_process_tree(pid: int) -> None:
    """Recursively kill a process and all its child processes cross-platform."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        parent.terminate()

        # Give 1 second for graceful termination
        gone, alive = psutil.wait_procs(children + [parent], timeout=1.0)
        for p in alive:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
    except psutil.NoSuchProcess:
        pass


def run_prolog_safe(
    args: List[str],
    default_engine: str = "scryer",
    default_timeout: str = "20s",
    default_memory: str = "50M",
    default_cpu_quota: str = "65%",
) -> int:
    """Run Prolog binary safely with cross-platform timeout, priority, and memory safeguards."""
    engine_name = os.environ.get("PROLOG_ENGINE", default_engine)
    timeout_str = os.environ.get("PROLOG_TIMEOUT", default_timeout)
    memory_str = os.environ.get("PROLOG_MEMORY_MAX", default_memory)
    cpu_quota_str = os.environ.get("PROLOG_CPU_QUOTA", default_cpu_quota)

    engine_bin = resolve_engine_binary(engine_name)
    bin_path = shutil.which(engine_bin)

    if not bin_path:
        sys.stderr.write(f"[prolog-safe] ERROR: Prolog engine binary '{engine_bin}' not found on PATH.\n")
        return 127

    timeout_sec = parse_timeout_seconds(timeout_str)
    memory_bytes = parse_memory_bytes(memory_str)
    system_name = platform.system()

    # On Linux, try systemd-run if available and cgroups active
    if system_name == "Linux" and shutil.which("systemd-run") and os.path.exists("/sys/fs/cgroup"):
        cmd = [
            "systemd-run",
            "--user",
            "--pty",
            f"--property=MemoryMax={memory_str}",
            f"--property=CPUQuota={cpu_quota_str}",
            f"--working-directory={os.getcwd()}",
            "timeout",
            "--foreground",
            f"{int(timeout_sec)}s",
            "nice",
            "-n",
            "19",
            bin_path,
        ] + args
        try:
            res = subprocess.run(cmd)
            return res.returncode
        except Exception:
            # Fall through to Python native execution on failure
            pass

    # Native Python execution with process tree supervision
    full_cmd = [bin_path] + args

    preexec_fn = None
    if system_name != "Windows":
        preexec_fn = lambda: set_process_limits_posix(memory_bytes)

    try:
        proc = psutil.Popen(
            full_cmd,
            preexec_fn=preexec_fn,
        )

        if system_name == "Windows":
            try:
                proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            except Exception:
                pass

        try:
            returncode = proc.wait(timeout=timeout_sec)
            return returncode
        except psutil.TimeoutExpired:
            sys.stderr.write(f"\n[prolog-safe] ERROR: Execution timed out after {timeout_sec}s. Terminating process tree.\n")
            kill_process_tree(proc.pid)
            return 124
    except KeyboardInterrupt:
        if 'proc' in locals():
            kill_process_tree(proc.pid)
        return 130
    except Exception as e:
        sys.stderr.write(f"[prolog-safe] Execution failed: {e}\n")
        return 1
