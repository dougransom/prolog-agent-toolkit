import os
import re
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


def parse_timeout_seconds(timeout_str: Optional[str], default: float = 20.0) -> float:
    """Parse timeout strings like '20s', '2m', '10' into seconds float."""
    if not timeout_str:
        return default
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
        return default


def next_fibonacci_increment(prev_fib: int = 3, current_fib: int = 5) -> tuple[int, int]:
    """Advance and return the next Fibonacci interval in sequence (e.g. (3, 5) -> (5, 8) -> (8, 13) -> (13, 21)...)."""
    next_fib = prev_fib + current_fib
    return current_fib, next_fib


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


def suspend_process_tree(pid: int) -> None:
    """Recursively suspend a process and all its child processes (zero CPU usage)."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.suspend()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        parent.suspend()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


def resume_process_tree(pid: int) -> None:
    """Recursively resume a suspended process and all its child processes."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.resume()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        parent.resume()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


def is_interactive_toplevel(args: List[str]) -> bool:
    """Determine if CLI invocation represents an interactive top-level session without batch goals."""
    for arg in args:
        if arg == "-g" or arg.startswith("-g"):
            return False
        if arg in ("-t", "-q") or arg.startswith("-t") or arg.startswith("-q"):
            return False
    return sys.stdin.isatty()


def extract_prolog_files_from_args(args: List[str]) -> List[str]:
    """Extract candidate Prolog file paths from CLI arguments and consult goals."""
    files = []
    for arg in args:
        if arg.endswith(".pl") or arg.endswith(".prolog"):
            if os.path.exists(arg):
                files.append(arg)
        elif "consult(" in arg:
            # Extract paths inside consult('path.pl') or consult("path.pl")
            matches = re.findall(r"consult\(['\"]([^'\"]+)['\"]\)", arg)
            for m in matches:
                if os.path.exists(m):
                    files.append(m)
    return list(dict.fromkeys(files))


def run_prolog_safe(
    args: List[str],
    default_engine: str = "scryer",
    default_timeout: str = "20s",
    default_memory: str = "500M",

    default_cpu_quota: str = "65%",
) -> int:
    """Run Prolog binary safely with cross-platform timeout, priority, memory safeguards, and syntax error diagnostics."""
    from prolog_agent_toolkit.syntax_checker import check_human_syntax_errors, format_syntax_diagnostics

    # Support standalone syntax check flag --check <file.pl>
    if "--check" in args:
        idx = args.index("--check")
        check_files = args[idx + 1:] if idx + 1 < len(args) else []
        if not check_files:
            check_files = extract_prolog_files_from_args(args)
        all_issues = []
        for f in check_files:
            if os.path.exists(f):
                all_issues.extend(check_human_syntax_errors(f))
        if all_issues:
            sys.stderr.write(format_syntax_diagnostics(all_issues))
            return 1
        else:
            sys.stdout.write("[prolog-safe] No obvious human syntax editing errors found.\n")
            return 0

    engine_name = os.environ.get("PROLOG_ENGINE", default_engine)
    timeout_str = os.environ.get("PROLOG_TIMEOUT", default_timeout)
    memory_str = os.environ.get("PROLOG_MEMORY_MAX", default_memory)
    cpu_quota_str = os.environ.get("PROLOG_CPU_QUOTA", default_cpu_quota)

    engine_bin = resolve_engine_binary(engine_name)
    bin_path = shutil.which(engine_bin)
    node_fallback_args = None

    if not bin_path:
        if engine_name.lower() in ("tau", "tau-prolog") and shutil.which("node"):
            bin_path = shutil.which("node")
            # Fallback to node execution for Tau Prolog
            sys.stdout.write("[prolog-safe] Notice: 'tau-prolog' binary not found. Using Node.js fallback runner.\n")
            # Build a JS snippet to require tau-prolog if available or evaluate basic query
            node_fallback_args = ["-e", "const tau = require('tau-prolog'); console.log('Tau Prolog Node runner ready');"]
        else:
            sys.stderr.write(f"[prolog-safe] ERROR: Prolog engine binary '{engine_bin}' not found on PATH.\n")
            return 127

    if is_interactive_toplevel(args) and "PROLOG_TIMEOUT" not in os.environ:
        timeout_sec = None
    else:
        timeout_sec = parse_timeout_seconds(timeout_str)
    memory_bytes = parse_memory_bytes(memory_str)
    system_name = platform.system()

    returncode = 0

    # On Linux, try systemd-run if available and cgroups active
    if system_name == "Linux" and shutil.which("systemd-run") and os.path.exists("/sys/fs/cgroup"):
        timeout_prefix = ["timeout", "--foreground", f"{int(timeout_sec)}s"] if timeout_sec is not None else []
        cmd = [
            "systemd-run",
            "--user",
            "--pty",
            f"--property=MemoryMax={memory_str}",
            f"--property=CPUQuota={cpu_quota_str}",
            f"--working-directory={os.getcwd()}",
        ] + timeout_prefix + [
            "nice",
            "-n",
            "19",
            bin_path,
        ] + args
        try:
            res = subprocess.run(cmd)
            returncode = res.returncode
        except Exception:
            # Fall through to Python native execution on failure
            pass

    if returncode == 0 and 'res' not in locals():
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
            except psutil.TimeoutExpired:
                sys.stderr.write(f"\n[prolog-safe] ERROR: Execution timed out after {timeout_sec}s. Terminating process tree.\n")
                kill_process_tree(proc.pid)
                returncode = 124
        except KeyboardInterrupt:
            if 'proc' in locals():
                kill_process_tree(proc.pid)
            returncode = 130
        except Exception as e:
            sys.stderr.write(f"[prolog-safe] Execution failed: {e}\n")
            returncode = 1

    # On compilation or execution failure, run diagnostic check on target Prolog files
    if returncode != 0:
        target_files = extract_prolog_files_from_args(args)
        all_issues = []
        for file_path in target_files:
            all_issues.extend(check_human_syntax_errors(file_path))
        if all_issues:
            sys.stderr.write(format_syntax_diagnostics(all_issues))

    return returncode

