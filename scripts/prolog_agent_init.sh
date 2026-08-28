#!/usr/bin/env bash
# PROLOG AGENT TOOLKIT — DIALECT-AWARE PROJECT INITIALIZER SCRIPT
# POSIX-compliant bash script for scaffolding Scryer, SWI, or Trealla Prolog projects.

set -euo pipefail

usage() {
    echo "Usage: $0 <project-name> [--dialect scryer|swi|trealla]"
    exit 1
}

if [ "$#" -lt 1 ]; then
    usage
fi

PROJECT_NAME="$1"
shift

DIALECT="scryer"
while [ "$#" -gt 0 ]; do
    case "$1" in
        --dialect|-d)
            DIALECT="$2"
            shift 2
            ;;
        scryer|swi|trealla)
            DIALECT="$1"
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            usage
            ;;
    esac
done

echo "====================================================================="
echo "Initializing Prolog Project: '${PROJECT_NAME}' (Dialect: ${DIALECT})"
echo "====================================================================="

# 1. Create directories
mkdir -p "${PROJECT_NAME}/src" "${PROJECT_NAME}/tests"

# 2. Link agent skills
TOOLKIT_AGENTS="${HOME}/code/prolog-agent-toolkit/.agents"
if [ -d "${TOOLKIT_AGENTS}" ]; then
    ln -s "${TOOLKIT_AGENTS}" "${PROJECT_NAME}/.agents" 2>/dev/null || true
    echo "Linked .agents -> ${TOOLKIT_AGENTS}"
fi

# 3. Dialect packaging
if [ "${DIALECT}" = "scryer" ]; then
    cat << EOF > "${PROJECT_NAME}/bakage.toml"
name = "${PROJECT_NAME}"
version = "0.1.0"
modules = ["src/${PROJECT_NAME}.pl"]
requires = []
EOF
    cat << EOF > "${PROJECT_NAME}/pack.pl"
name('${PROJECT_NAME}').
version('0.1.0').
title('${PROJECT_NAME} Prolog library').
author('Developer').
EOF
elif [ "${DIALECT}" = "swi" ]; then
    cat << EOF > "${PROJECT_NAME}/pack.pl"
name('${PROJECT_NAME}').
version('0.1.0').
title('${PROJECT_NAME} SWI-Prolog library').
author('Developer', 'dev@example.com').
home('https://example.com').
requires([]).
EOF
elif [ "${DIALECT}" = "trealla" ]; then
    echo "Trealla Prolog dialect selected: skipping package manifest (no package manager)."
fi

# 4. Starter module src/<project-name>.pl
if [ "${DIALECT}" = "swi" ]; then
    cat << EOF > "${PROJECT_NAME}/src/${PROJECT_NAME}.pl"
:- module(${PROJECT_NAME}, [
    hello/1,
    parse_item//1,
    solve_range/2
]).

:- use_module(library(clpfd)).

%%  hello(-Greeting:chars) is det.
%   Generates standard greeting string.
hello("Hello from ${PROJECT_NAME}!").

%%  parse_item(-Item:chars)// is det.
%   Pure DCG rule for parsing an item tag.
parse_item(Item) -->
    "[", Item, "]".

%%  solve_range(+N:integer, -X:integer) is semidet.
%   CLP(FD) integer constraint example.
solve_range(N, X) :-
    X #>= 0,
    X #=< N,
    X #= N - 1.
EOF
elif [ "${DIALECT}" = "trealla" ]; then
    cat << EOF > "${PROJECT_NAME}/src/${PROJECT_NAME}.pl"
% Trealla Prolog Module: ${PROJECT_NAME}

:- use_module(library(charsio)).
:- use_module(library(dcgs)).

%%  hello(-Greeting:chars) is det.
%   Generates standard greeting string.
hello("Hello from ${PROJECT_NAME}!").

%%  parse_item(-Item:chars)// is det.
%   Pure DCG rule for parsing an item tag.
parse_item(Item) -->
    "[", Item, "]".
EOF
else
    # Scryer / ISO (default)
    cat << EOF > "${PROJECT_NAME}/src/${PROJECT_NAME}.pl"
:- module(${PROJECT_NAME}, [
    hello/1,
    parse_item//1,
    solve_range/2
]).

:- use_module(library(charsio)).
:- use_module(library(dcgs)).
:- use_module(library(clpz)).
:- use_module(library(reif)).

%%  hello(-Greeting:chars) is det.
%   Generates standard greeting string.
hello("Hello from ${PROJECT_NAME}!").

%%  parse_item(-Item:chars)// is det.
%   Pure DCG rule for parsing an item tag.
parse_item(Item) -->
    "[", Item, "]".

%%  solve_range(+N:integer, -X:integer) is semidet.
%   CLP(Z) integer constraint example.
solve_range(N, X) :-
    X #>= 0,
    X #=< N,
    X #= N - 1.
EOF
fi

# 5. Testing scaffolding
if [ "${DIALECT}" = "swi" ]; then
    cat << EOF > "${PROJECT_NAME}/tests/test_${PROJECT_NAME}.pl"
:- use_module(library(plunit)).
:- use_module('../src/${PROJECT_NAME}.pl').

:- begin_tests(${PROJECT_NAME}).

test(hello) :-
    hello(Msg),
    assertion(Msg \== []).

test(dcg_parse) :-
    phrase(parse_item("test"), "[test]").

:- end_tests(${PROJECT_NAME}).
EOF
else
    cat << EOF > "${PROJECT_NAME}/tests/testing.pl"
:- use_module(library(format)).
:- use_module(library(dcgs)).
:- use_module('../src/${PROJECT_NAME}.pl').

:- initialization(run_tests).

run_tests :-
    hello(Msg),
    format("Test hello/1 passed: ~s~n", [Msg]),
    (   phrase(parse_item("abc"), "[abc]") ->
        format("Test parse_item//1 passed.~n", [])
    ;   format("Test parse_item//1 failed!~n", []),
        halt(1)
    ).
EOF
fi

# 6. CHANGELOG.md & README.md
cat << EOF > "${PROJECT_NAME}/CHANGELOG.md"
# Changelog

All notable changes to \`${PROJECT_NAME}\` will be documented in this file.

## [0.1.0] - $(date +%Y-%m-%d)
- Initial release of \`${PROJECT_NAME}\`.
EOF

MANIFEST_FILE="bakage.toml"
TEST_FILE="testing.pl"
RUNNER_CMD="scryer-safe -g \"use_module('src/${PROJECT_NAME}.pl'), hello(M), write(M), nl, halt.\""
TEST_CMD="scryer-safe tests/testing.pl"
DIALECT_NAME="Scryer Prolog"
SKILL_REF="\`.agents/skills/scryer-prolog-standards/SKILL.md\` and \`.agents/skills/prolog-conventions/SKILL.md\`"

if [ "${DIALECT}" = "swi" ]; then
    MANIFEST_FILE="pack.pl"
    TEST_FILE="test_${PROJECT_NAME}.pl"
    RUNNER_CMD="swi-safe -g \"use_module('src/${PROJECT_NAME}.pl'), hello(M), writeln(M), halt.\""
    TEST_CMD="swi-safe -g \"run_tests,halt\" tests/test_${PROJECT_NAME}.pl"
    DIALECT_NAME="SWI-Prolog"
    SKILL_REF="\`.agents/skills/swi-prolog-standards/SKILL.md\` and \`.agents/skills/prolog-conventions/SKILL.md\`"
elif [ "${DIALECT}" = "trealla" ]; then
    MANIFEST_FILE="pack.pl"
    TEST_FILE="testing.pl"
    RUNNER_CMD="trealla-safe -g \"use_module('src/${PROJECT_NAME}.pl'), hello(M), write(M), nl, halt.\""
    TEST_CMD="trealla-safe tests/testing.pl"
    DIALECT_NAME="Trealla Prolog"
    SKILL_REF="\`.agents/skills/trealla-prolog-standards/SKILL.md\` and \`.agents/skills/prolog-conventions/SKILL.md\`"
fi

cat << EOF > "${PROJECT_NAME}/README.md"
# ${PROJECT_NAME}

> Powered by [prolog-agent-toolkit](https://github.com/dougransom/prolog-agent-toolkit) **v0.0.1.dev6**

A modern Prolog project configured for deterministic execution, engine safety, and automated AI agent collaboration.

---

## 1. Project Overview

This project uses **\`prolog-agent-toolkit\` (v0.0.1.dev6)**.

The \`prolog-agent-toolkit\` provides a standardized development environment for writing safe, pure, high-quality Prolog software. Its primary capabilities include:

- **Deterministic Safe Runners**: Cross-platform command-line entry points (\`scryer-safe\`, \`swi-safe\`, \`trealla-safe\`, \`tau-safe\`, \`prolog-safe\`) that run Prolog execution under strict CPU and memory resource limits.
- **Dialect Standards & Purity**: Enforced coding guidelines, Covington style standards, reified logical predicates (\`if_/3\`, \`dif/2\`), pure DCGs, and CLP constraint logic.
- **Agent Skill Architecture**: Integrated \`.agents/\` directory providing structured skills and linting rules so AI assistants (e.g. Gemini, Cursor, Claude, Copilot) generate pure, idiomatic code.
- **Multi-Engine Support**: Seamless portability across Prolog engines (Scryer Prolog, SWI-Prolog, Trealla Prolog, Tau Prolog).

---

## 2. Directory Layout

Recommended project structure:

\`\`\`text
${PROJECT_NAME}/
├── src/
│   └── ${PROJECT_NAME}.pl      # Main module source file
├── tests/
│   └── ${TEST_FILE}         # Unit test suite
├── .agents -> /path/to/prolog-agent-toolkit/.agents # Symlink to shared agent skills & rules
├── ${MANIFEST_FILE}              # Packaging manifest
├── CHANGELOG.md               # Version release history
└── README.md                  # Developer & AI agent onboarding guide
\`\`\`

### Directory Roles

- **\`src/\`**: Houses application and library Prolog source files. Modules explicitly declare exports and follow pure ISO standards.
- **\`tests/\`**: Contains unit test harnesses and test cases.
- **\`.agents/\`**: Workspace symlink pointing to the shared \`prolog-agent-toolkit/.agents\` directory. Gives AI coding agents immediate access to project guidelines, dialect rules, refactoring subagents, and linter specifications.
- **\`${MANIFEST_FILE}\`**: Packaging manifest file.
- **\`README.md\`**: Canonical onboarding document for developers and AI agents.

---

## 3. Dialect Selection

This project is configured to use **${DIALECT_NAME}**.

### Dialect Overview
Adheres to engine standards and logical purity conventions.

### Dialect Standards Reference
When writing code or directing AI agents, consult the dialect standards provided by the toolkit:
- **Primary Dialect Skill**: ${SKILL_REF}
- **Universal Style Guide**: \`.agents/references/covington_style.md\`
- **Purity Guidelines**: \`.agents/references/prolog_guidelines.md\`

---

## 4. Safe Runners

All Prolog executions **MUST** use the safe runner entry points provided by \`prolog-agent-toolkit\`. Developers and AI agents MUST NEVER invoke raw binary interpreters directly (e.g. \`scryer-prolog\`, \`swipl\`, \`tpl\`).

### Executing Code

\`\`\`bash
# Run goal safely using the target runner:
${RUNNER_CMD}

# Run using generic wrapper (select engine via environment variable):
export PROLOG_ENGINE=${DIALECT}
prolog-safe -g "hello(M), write(M), nl, halt." src/${PROJECT_NAME}.pl
\`\`\`

### Why Safe Runners Are Required

1. **Resource Sandboxing**: Prevents non-terminating recursive searches or infinite choice-point backtracking loops from locking up CPU cores or exhausting system memory.
2. **Environment Determinism**: Standardizes standard library module imports, string encoding, and error reporting across environments.
3. **Execution Safety**: Enforces safety policies required for agent-driven autonomous execution.

---

## 5. Agent Skills Architecture

The \`.agents/\` directory connects this repository to the \`prolog-agent-toolkit\` knowledge base.

### How \`.agents\` Is Used
- **Shared via Symlink**: Link the toolkit's \`.agents\` directory during workspace setup:
  \`\`\`bash
  ln -s ~/code/prolog-agent-toolkit/.agents .agents
  \`\`\`
- **Deterministic Assistant Behavior**: When an AI coding assistant operates in this project, it automatically reads \`.agents/AGENTS.md\` and active skills to enforce pure Prolog standards, first-argument indexing, and Covington styling.
- **Modular Capabilities**: Exposes automated skills for static analysis, unit test generation, DCG mastery, CLP constraints, and release management.

---

## 6. Testing

### Running Tests

Execute the unit test suite using the appropriate safe runner:

\`\`\`bash
${TEST_CMD}
\`\`\`
EOF

echo "Project '${PROJECT_NAME}' successfully initialized!"

