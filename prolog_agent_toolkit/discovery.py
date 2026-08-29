import os
import sys
import json
import re
import shutil
import subprocess
from typing import List, Dict, Any, Optional

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


STATIC_LIBRARY_DATABASE: Dict[str, List[Dict[str, str]]] = {
    "scryer": [
        {
            "name": "dcgs",
            "import": ":- use_module(library(dcgs)).",
            "exports": "phrase/2, phrase/3, seq//1, seq_with//2",
            "description": "Definite Clause Grammar (DCG) parsing and sequence processing.",
            "category": "parsing"
        },
        {
            "name": "charsio",
            "import": ":- use_module(library(charsio)).",
            "exports": "read_from_chars/2, write_to_chars/2, get_single_char/1",
            "description": "Character list I/O (Scryer represents strings as character lists).",
            "category": "io"
        },
        {
            "name": "reif",
            "import": ":- use_module(library(reif)).",
            "exports": "if_/3, dif/2, (=)/3, memberd_t/3, tfilter/3",
            "description": "Pure reified logical conditionals and sound term inequality.",
            "category": "logic"
        },
        {
            "name": "clpz",
            "import": ":- use_module(library(clpz)).",
            "exports": "(#=)/2, (#\\/)/2, label/1, labeling/2, zcompare/3",
            "description": "Constraint Logic Programming over Integers CLP(Z).",
            "category": "constraints"
        },
        {
            "name": "si",
            "import": ":- use_module(library(si)).",
            "exports": "list_si/1, atom_si/1, integer_si/1, chars_si/1",
            "description": "Monotonic, safe type testing predicates (safely instantiated).",
            "category": "types"
        },
        {
            "name": "lambda",
            "import": ":- use_module(library(lambda)).",
            "exports": "\\X^..., \\X^Y^Goal",
            "description": "Anonymous lambda expression syntax for higher-order goals.",
            "category": "higher_order"
        },
        {
            "name": "format",
            "import": ":- use_module(library(format)).",
            "exports": "format/2, format/3, portray_clause/1",
            "description": "Formatted output with format control sequences.",
            "category": "io"
        },
        {
            "name": "lists",
            "import": ":- use_module(library(lists)).",
            "exports": "member/2, select/3, append/3, length/2, reverse/2",
            "description": "Pure list manipulation utilities.",
            "category": "data_structures"
        },
        {
            "name": "assoc",
            "import": ":- use_module(library(assoc)).",
            "exports": "empty_assoc/1, get_assoc/3, put_assoc/4",
            "description": "AVL-tree key-value association maps.",
            "category": "data_structures"
        },
        {
            "name": "between",
            "import": ":- use_module(library(between)).",
            "exports": "between/3",
            "description": "Integer range generation and iteration.",
            "category": "iteration"
        },
        {
            "name": "time",
            "import": ":- use_module(library(time)).",
            "exports": "time/1, current_time/1",
            "description": "Execution timing and timestamping.",
            "category": "system"
        },
        {
            "name": "random",
            "import": ":- use_module(library(random)).",
            "exports": "maybe/0, random_integer/3",
            "description": "Pseudorandom number generation.",
            "category": "math"
        }
    ],
    "swi": [
        {
            "name": "clpfd",
            "import": ":- use_module(library(clpfd)).",
            "exports": "(#=)/2, in/2, label/1, labeling/2",
            "description": "Constraint Logic Programming over Finite Domains.",
            "category": "constraints"
        },
        {
            "name": "yall",
            "import": ":- use_module(library(yall)).",
            "exports": "[X]>>..., [X,Y]>>Goal",
            "description": "SWI built-in lambda syntax (yall).",
            "category": "higher_order"
        },
        {
            "name": "apply",
            "import": ":- use_module(library(apply)).",
            "exports": "maplist/2..5, include/3, exclude/3, foldl/4",
            "description": "Higher-order list mapping and filtering.",
            "category": "higher_order"
        },
        {
            "name": "dcg/basics",
            "import": ":- use_module(library(dcg/basics)).",
            "exports": "string//1, integer//1, whites//0",
            "description": "Common DCG parsing non-terminals.",
            "category": "parsing"
        },
        {
            "name": "ordsets",
            "import": ":- use_module(library(ordsets)).",
            "exports": "list_to_ord_set/2, ord_union/3",
            "description": "Ordered set operations on sorted lists.",
            "category": "data_structures"
        },
        {
            "name": "plunit",
            "import": ":- use_module(library(plunit)).",
            "exports": ":- begin_tests(name)., :- end_tests(name).",
            "description": "Native SWI unit testing framework.",
            "category": "testing"
        },
        {
            "name": "dicts",
            "import": "% Built-in SWI Dicts",
            "exports": "get_dict/3, put_dict/4, is_dict/1",
            "description": "Native SWI dictionary support (Dict.Key syntax).",
            "category": "data_structures"
        }
    ],
    "trealla": [
        {
            "name": "dcgs",
            "import": ":- use_module(library(dcgs)).",
            "exports": "phrase/2, phrase/3",
            "description": "ISO Definite Clause Grammar rules.",
            "category": "parsing"
        },
        {
            "name": "charsio",
            "import": ":- use_module(library(charsio)).",
            "exports": "read_from_chars/2, write_to_chars/2",
            "description": "Character list I/O.",
            "category": "io"
        },
        {
            "name": "clpz",
            "import": ":- use_module(library(clpz)).",
            "exports": "(#=)/2, label/1, labeling/2",
            "description": "Trealla integer arithmetic constraints.",
            "category": "constraints"
        },
        {
            "name": "reif",
            "import": ":- use_module(library(reif)).",
            "exports": "if_/3, dif/2, (=)/3",
            "description": "Reified conditional logic.",
            "category": "logic"
        },
        {
            "name": "when",
            "import": ":- use_module(library(when)).",
            "exports": "when/2, freeze/2",
            "description": "Goal suspension and coroutining.",
            "category": "control"
        },
        {
            "name": "format",
            "import": ":- use_module(library(format)).",
            "exports": "format/2, format/3",
            "description": "Formatted string/stdout printing.",
            "category": "io"
        },
        {
            "name": "random",
            "import": ":- use_module(library(random)).",
            "exports": "maybe/0, random_integer/3",
            "description": "Fast pseudorandom generation.",
            "category": "math"
        }
    ],
    "tau": [
        {
            "name": "dom",
            "import": ":- use_module(library(dom)).",
            "exports": "get_by_id/2, set_html/2, add_event_listener/3",
            "description": "Browser DOM element manipulation.",
            "category": "web"
        },
        {
            "name": "js",
            "import": ":- use_module(library(js)).",
            "exports": "eval/2, global/2, prop/3",
            "description": "JavaScript object and global environment interop.",
            "category": "interop"
        },
        {
            "name": "lists",
            "import": ":- use_module(library(lists)).",
            "exports": "member/2, append/3, length/2",
            "description": "Core ISO list predicates.",
            "category": "data_structures"
        },
        {
            "name": "format",
            "import": ":- use_module(library(format)).",
            "exports": "format/2, format/3",
            "description": "Formatted output.",
            "category": "io"
        },
        {
            "name": "random",
            "import": ":- use_module(library(random)).",
            "exports": "random/1, random_integer/3",
            "description": "JavaScript-backed random generator.",
            "category": "math"
        }
    ],
    "gnu": [
        {
            "name": "lists",
            "import": "% Built-in list predicates",
            "exports": "member/2, append/3, length/2",
            "description": "Standard GNU Prolog list predicates.",
            "category": "data_structures"
        },
        {
            "name": "fd",
            "import": "% Built-in FD solver",
            "exports": "fd_domain/3, fd_labeling/1, fd_has_extra_domain/1",
            "description": "GNU Prolog built-in finite domain constraint solver.",
            "category": "constraints"
        }
    ]
}


def discover_manifest_packages(project_dir: str = ".") -> List[Dict[str, Any]]:
    """Scan local directory for package manifest files (scryer-manifest.pl, pack.pl, package.json)."""
    manifests = []

    # 1. scryer-manifest.pl
    scryer_manifest_path = os.path.join(project_dir, "scryer-manifest.pl")
    if os.path.exists(scryer_manifest_path):
        with open(scryer_manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
        name_match = re.search(r"name\(\s*[\"\']?([a-zA-Z0-9_\-]+)[\"\']?\s*\)", content)
        deps_match = re.search(r"dependencies\(\s*\[(.*?)\]\s*\)", content, re.DOTALL)
        deps = []
        if deps_match:
            deps = [d.strip(' "\'\t\n') for d in deps_match.group(1).split(",") if d.strip(' "\'\t\n')]
        manifests.append({
            "source": "scryer-manifest.pl",
            "name": name_match.group(1) if name_match else os.path.basename(os.path.abspath(project_dir)),
            "engine": "scryer",
            "dependencies": deps
        })

    # 2. pack.pl
    pack_path = os.path.join(project_dir, "pack.pl")
    if os.path.exists(pack_path):
        with open(pack_path, "r", encoding="utf-8") as f:
            content = f.read()
        name_match = re.search(r"name\(['\"]?([^'\")]+)['\"]?\)\.", content)
        deps_match = re.search(r"dependencies\(\[(.*?)\]\)\.", content, re.DOTALL)
        deps = []
        if deps_match:
            deps = [d.strip(' "\'\t\n') for d in deps_match.group(1).split(",") if d.strip(' "\'\t\n')]
        manifests.append({
            "source": "pack.pl",
            "name": name_match.group(1) if name_match else os.path.basename(os.path.abspath(project_dir)),
            "engine": "swi",
            "dependencies": deps
        })

    # 3. package.json
    pkg_path = os.path.join(project_dir, "package.json")
    if os.path.exists(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            deps = list(data.get("dependencies", {}).keys()) + list(data.get("devDependencies", {}).keys())
            manifests.append({
                "source": "package.json",
                "name": data.get("name", os.path.basename(os.path.abspath(project_dir))),
                "engine": "tau",
                "dependencies": deps
            })
        except Exception:
            pass

    return manifests


def discover_runtime_engine_modules(engine: str) -> List[str]:
    """Interrogate running Prolog engine for dynamic module list via safe execution runner."""
    from prolog_agent_toolkit.runner import resolve_engine_binary

    engine = engine.lower().strip()
    bin_name = resolve_engine_binary(engine)
    if not shutil.which(bin_name):
        return []

    # Safe introspective query command per engine
    goals = {
        "scryer": "current_module(M), write(M), nl, fail; true, halt.",
        "swi": "forall(current_module(M), (write(M), nl)), halt.",
        "trealla": "current_module(M), write(M), nl, fail; true, halt.",
        "tau": "current_module(M), write(M), nl, fail; true, halt.",
        "gnu": "true, halt."
    }

    goal = goals.get(engine)
    if not goal:
        return []

    try:
        env = os.environ.copy()
        env["PROLOG_ENGINE"] = engine
        cmd = [bin_name, "-g", goal]
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5.0,
            env=env
        )
        if res.returncode == 0 and res.stdout:
            modules = [line.strip() for line in res.stdout.splitlines() if line.strip() and not line.startswith("[")]
            return sorted(list(dict.fromkeys(modules)))
    except Exception:
        pass

    return []


def discover_capabilities(
    engine: str = "all",
    query: Optional[str] = None,
    mode: str = "hybrid",
    project_dir: str = "."
) -> Dict[str, Any]:
    """
    Discover available Prolog libraries, modules, and packages across static database,
    local project manifests, and runtime engine introspection.
    """
    target_engines = ["scryer", "swi", "trealla", "tau", "gnu"] if engine in ("all", "iso") else [engine.lower()]

    results: Dict[str, Any] = {
        "query": query,
        "mode": mode,
        "engines": {}
    }

    query_norm = query.lower().strip() if query else None

    manifests = discover_manifest_packages(project_dir=project_dir)

    for eng in target_engines:
        static_libs = STATIC_LIBRARY_DATABASE.get(eng, [])
        filtered_static = []

        for lib in static_libs:
            if not query_norm:
                filtered_static.append(lib)
            else:
                text = f"{lib['name']} {lib['import']} {lib['exports']} {lib['description']} {lib['category']}".lower()
                if query_norm in text:
                    filtered_static.append(lib)

        eng_manifests = [m for m in manifests if m["engine"] == eng or eng == "all"]

        runtime_modules = []
        if mode in ("hybrid", "dynamic"):
            runtime_modules = discover_runtime_engine_modules(eng)
            if query_norm:
                runtime_modules = [m for m in runtime_modules if query_norm in m.lower()]

        results["engines"][eng] = {
            "static_libraries": filtered_static,
            "manifests": eng_manifests,
            "runtime_modules": runtime_modules
        }

    return results


def format_discovery_report(data: Dict[str, Any]) -> str:
    """Format discovery results into clean human-readable Markdown report."""
    query = data.get("query")
    lines = []
    lines.append("==================================================================")
    lines.append("PROLOG AGENT TOOLKIT — LIBRARY & CAPABILITY DISCOVERY REPORT")
    lines.append("==================================================================")
    if query:
        lines.append(f"Search Query: '{query}'")
    lines.append(f"Discovery Mode: {data.get('mode', 'hybrid').upper()}\n")

    for eng, info in data.get("engines", {}).items():
        lines.append(f"--- ENGINE: {eng.upper()} PROLOG ---")

        # 1. Static Standard Libraries
        libs = info.get("static_libraries", [])
        if libs:
            lines.append("  Standard Libraries & Modules:")
            for lib in libs:
                lines.append(f"  • {lib['name']:<15} | {lib['import']:<38} | {lib['description']}")
                lines.append(f"    Exports: {lib['exports']}\n")
        else:
            lines.append("  Standard Libraries: (None matched query)\n")

        # 2. Local Manifests
        mans = info.get("manifests", [])
        if mans:
            lines.append("  Local Project Manifests:")
            for m in mans:
                lines.append(f"  • File: {m['source']} (Package: {m['name']})")
                if m['dependencies']:
                    lines.append(f"    Declared Dependencies: {', '.join(m['dependencies'])}")
            lines.append("")

        # 3. Dynamic Runtime Modules
        rt_mods = info.get("runtime_modules", [])
        if rt_mods:
            lines.append("  Dynamic Runtime Modules:")
            lines.append(f"  • {', '.join(rt_mods)}\n")

    lines.append("==================================================================")
    lines.append("PRE-CODE-GENERATION POLICY REMINDER:")
    lines.append("1. Prefer discovered built-in libraries over custom predicate code.")
    lines.append("2. Always explicitly declare `:- use_module(library(...)).` headers.")
    lines.append("3. Document chosen dependencies and rationale in Covington module headers.")
    lines.append("==================================================================")

    return "\n".join(lines)
