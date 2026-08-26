:- module(initializer, [
    init_project_spec/3,
    generate_module_spec/3,
    generate_template_spec/3,
    init_script_spec/1,
    bakage_manifest//2,
    pack_manifest//2,
    starter_module//2,
    test_scaffold//2,
    readme_scaffold//2
]).

:- use_module(library(dcgs)).
:- use_module(library(charsio)).
:- use_module(library(format)).
:- use_module(library(lists)).

%%  init_project_spec(+ProjectName:chars, +Dialect:atom, -Files:list) is det.
%   Generates abstract file specification list for a new Prolog project.
%   Files is a list of file(Path, ContentChars).
init_project_spec(ProjectName, Dialect, Files) :-
    bakage_manifest(ProjectName, "0.1.0", BakageChars, []),
    pack_manifest(ProjectName, "0.1.0", PackChars, []),
    starter_module(ProjectName, Dialect, ModChars, []),
    test_scaffold(ProjectName, Dialect, TestChars, []),
    readme_scaffold(ProjectName, Dialect, ReadmeChars, []),
    (   Dialect = swi ->
        TestPath = "tests/test_" ++ ProjectName ++ ".pl",
        Files = [
            file("pack.pl", PackChars),
            file("src/" ++ ProjectName ++ ".pl", ModChars),
            file(TestPath, TestChars),
            file("README.md", ReadmeChars),
            file("CHANGELOG.md", "# Changelog\n\nAll notable changes will be documented in this file.\n")
        ]
    ;   Dialect = trealla ->
        Files = [
            file("src/" ++ ProjectName ++ ".pl", ModChars),
            file("tests/testing.pl", TestChars),
            file("README.md", ReadmeChars),
            file("CHANGELOG.md", "# Changelog\n\nAll notable changes will be documented in this file.\n")
        ]
    ;   % Default Scryer / ISO
        Files = [
            file("bakage.toml", BakageChars),
            file("pack.pl", PackChars),
            file("src/" ++ ProjectName ++ ".pl", ModChars),
            file("tests/testing.pl", TestChars),
            file("README.md", ReadmeChars),
            file("CHANGELOG.md", "# Changelog\n\nAll notable changes will be documented in this file.\n")
        ]
    ).

%%  generate_module_spec(+ModuleName:chars, +Dialect:atom, -ContentChars:chars) is det.
%   Generates content for a new Prolog module stub.
generate_module_spec(ModuleName, Dialect, ContentChars) :-
    phrase(starter_module(ModuleName, Dialect), ContentChars).

%%  generate_template_spec(+ProjectName:chars, +Dialect:atom, -Files:list) is det.
%   Generates file specifications for standard project template layout.
generate_template_spec(ProjectName, Dialect, Files) :-
    init_project_spec(ProjectName, Dialect, Files).

%%  init_script_spec(-ScriptChars:chars) is det.
%   Generates POSIX-compatible bash initialization script specification.
init_script_spec(ScriptChars) :-
    phrase(init_bash_script, ScriptChars).

% --- DCG Generators ---

bakage_manifest(ProjectName, Version) -->
    "name = \"", ProjectName, "\"\n",
    "version = \"", Version, "\"\n",
    "modules = [\"src/", ProjectName, ".pl\"]\n",
    "requires = []\n".

pack_manifest(ProjectName, Version) -->
    "name('", ProjectName, "').\n",
    "version('", Version, "').\n",
    "title('", ProjectName, " Prolog library').\n",
    "author('Developer', 'dev@example.com').\n",
    "home('https://example.com').\n",
    "requires([]).\n".

starter_module(ModuleName, Dialect) -->
    (   { Dialect = swi } ->
        ":- module(", ModuleName, ", [\n",
        "    hello/1,\n",
        "    parse_item//1,\n",
        "    solve_range/2\n",
        "]).\n\n",
        ":- use_module(library(clpfd)).\n\n"
    ;   { Dialect = trealla } ->
        "% Trealla Prolog Module: ", ModuleName, "\n\n",
        ":- use_module(library(charsio)).\n",
        ":- use_module(library(dcgs)).\n\n"
    ;   % Scryer / ISO
        ":- module(", ModuleName, ", [\n",
        "    hello/1,\n",
        "    parse_item//1,\n",
        "    solve_range/2\n",
        "]).\n\n",
        ":- use_module(library(charsio)).\n",
        ":- use_module(library(dcgs)).\n",
        ":- use_module(library(clpz)).\n",
        ":- use_module(library(reif)).\n\n"
    ),
    "%%\thello(-Greeting:chars) is det.\n",
    "%\tGenerates a standard greeting string.\n",
    "hello(\"Hello from ", ModuleName, "!\").\n\n",
    "%%\tparse_item(-Item:chars)// is det.\n",
    "%\tPure DCG rule for parsing an item tag.\n",
    "parse_item(Item) -->\n",
    "    \"[\", Item, \"]\".\n\n",
    "%%\tsolve_range(+N:integer, -X:integer) is semidet.\n",
    "%\tCLP(Z)/CLP(FD) integer constraint example.\n",
    "solve_range(N, X) :-\n",
    "    X #>= 0,\n",
    "    X #=< N,\n",
    "    X #= N - 1.\n".

test_scaffold(ProjectName, Dialect) -->
    (   { Dialect = swi } ->
        ":- use_module(library(plunit)).\n",
        ":- use_module('../src/", ProjectName, ".pl').\n\n",
        ":- begin_tests(", ProjectName, ").\n\n",
        "test(hello) :-\n",
        "    hello(Msg),\n",
        "    assertion(Msg \\== []).\n\n",
        "test(dcg_parse) :-\n",
        "    phrase(parse_item(\"test\"), \"[test]\").\n\n",
        ":- end_tests(", ProjectName, ").\n"
    ;   % Scryer / Trealla / ISO
        ":- use_module(library(format)).\n",
        ":- use_module(library(dcgs)).\n",
        ":- use_module('../src/", ProjectName, ".pl').\n\n",
        ":- initialization(run_tests).\n\n",
        "run_tests :-\n",
        "    hello(Msg),\n",
        "    format(\"Test hello/1 passed: ~s~n\", [Msg]),\n",
        "    (   phrase(parse_item(\"abc\"), \"[abc]\") ->\n",
        "        format(\"Test parse_item//1 passed.~n\", [])\n",
        "    ;   format(\"Test parse_item//1 failed!~n\", []),\n",
        "        halt(1)\n",
        "    ).\n"
    ).

readme_scaffold(ProjectName, Dialect) -->
    "# ", ProjectName, "\n\n",
    "Prolog project `", ProjectName, "` initialized for dialect `", Dialect, "`.\n\n",
    "## Quick Start\n\n",
    "### Running Unit Tests\n\n",
    (   { Dialect = swi } ->
        "Run SWI-Prolog unit tests:\n```bash\nswi-safe -g \"run_tests,halt\" tests/test_", ProjectName, ".pl\n```\n\n"
    ;   "Run Scryer / ISO Prolog unit tests:\n```bash\nscryer-safe tests/testing.pl\n```\n\n"
    ),
    "### Agent Skills & Standards\n\n",
    "Ensure agent skills are symlinked:\n",
    "```bash\nln -s ~/code/prolog-agent-toolkit/.agents .agents\n```\n".

init_bash_script -->
    "#!/usr/bin/env bash\n",
    "# Prolog Agent Toolkit — POSIX Project Initializer Script\n",
    "set -euo pipefail\n\n",
    "PROJECT_NAME=\"${1:-myproj}\"\n",
    "DIALECT=\"${2:-scryer}\"\n\n",
    "echo \"Initializing Prolog project '${PROJECT_NAME}' (Dialect: ${DIALECT})...\"\n\n",
    "mkdir -p \"${PROJECT_NAME}/src\" \"${PROJECT_NAME}/tests\"\n\n",
    "if [ -d \"${HOME}/code/prolog-agent-toolkit/.agents\" ]; then\n",
    "    ln -s \"${HOME}/code/prolog-agent-toolkit/.agents\" \"${PROJECT_NAME}/.agents\" || true\n",
    "fi\n\n",
    "if [ \"${DIALECT}\" = \"scryer\" ]; then\n",
    "cat << 'EOF' > \"${PROJECT_NAME}/bakage.toml\"\n",
    "name = \"${PROJECT_NAME}\"\n",
    "version = \"0.1.0\"\n",
    "modules = [\"src/${PROJECT_NAME}.pl\"]\n",
    "requires = []\n",
    "EOF\n",
    "fi\n\n",
    "echo \"Project ${PROJECT_NAME} created successfully.\"\n".
