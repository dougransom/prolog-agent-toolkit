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

cat << EOF > "${PROJECT_NAME}/README.md"
# ${PROJECT_NAME}

Prolog project \`${PROJECT_NAME}\` initialized for dialect \`${DIALECT}\` using \`prolog-agent-toolkit\`.

## Running Tests

$(if [ "${DIALECT}" = "swi" ]; then
    echo "Run unit tests with \`swi-safe\`:"
    echo '```bash'
    echo "swi-safe -g \"run_tests,halt\" tests/test_${PROJECT_NAME}.pl"
    echo '```'
else
    echo "Run unit tests with \`scryer-safe\` or \`prolog-safe\`:"
    echo '```bash'
    echo "scryer-safe tests/testing.pl"
    echo '```'
fi)

## Safe Execution

Always execute Prolog code using cross-platform safety runners:
- \`prolog-safe\`
- \`scryer-safe\`
- \`swi-safe\`
- \`trealla-safe\`

## Agent Skills

Link toolkit agent skills:
\`\`\`bash
ln -s ~/code/prolog-agent-toolkit/.agents .agents
\`\`\`
EOF

echo "Project '${PROJECT_NAME}' successfully initialized!"
