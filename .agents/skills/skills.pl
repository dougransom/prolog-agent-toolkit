/** <module> skills
 *
 * Homoiconic Prolog skill capability registry for the Prolog Agent Toolkit.
 * Represents skills and their capabilities as queryable Prolog facts.
 *
 * @author Doug Ransom
 * @license Unlicense
 */

:- module(skills, [
    skill/2,
    skill_path/2,
    skill_capability/2,
    find_skills_by_capability/2
]).

:- use_module(library(lists), [member/2]).

%% skill(?SkillName:atom, ?Capabilities:list(atom)) is nondet.
%  Registered skills and their respective capability tags.
skill(prolog_conventions,            [purity, dcg, clp, type_testing, strings, iso_compliance]).
skill(prolog_code_review,            [code_review, purity, determinism, portability, safety, testing]).
skill(prolog_clp_constraints,        [clp, clpz, clpfd, scheduling, optimization, labeling]).
skill(prolog_dcg_mastery,            [dcg, parsing, lexing, ast, formatting, serialization]).
skill(prolog_debugging_workflow,     [debugging, tracing, spy_points, execution_inspection]).
skill(prolog_declarative_workflow,   [declarative_reasoning, test_driven, modes, determinism]).
skill(prolog_engine_onboarding,      [engine_onboarding, multi_engine, runner_scaffolding]).
skill(prolog_ffi_wasm_embedding,     [ffi, wasm, c_interop, rust_interop, python_interop, js_interop]).
skill(prolog_initializer,            [scaffolding, project_init, template_generation, module_generation]).
skill(prolog_library_discovery,      [library_discovery, module_search, dependency_resolution]).
skill(prolog_linter_static_analysis, [linting, static_analysis, singleton_detection, safety]).
skill(prolog_migrate_project,        [migration, legacy_upgrade, refactoring, worktree]).
skill(prolog_neurosymbolic_agent,    [neurosymbolic, llm_integration, formal_verification, ground_truth]).
skill(prolog_packaging,              [packaging, bakage, pack_install, manifests]).
skill(prolog_performance_profiling,  [profiling, indexing, choicepoints, tail_recursion, reif]).
skill(prolog_release,                [release_management, versioning, git_tagging, manifest_sync]).
skill(prolog_tabling,                [tabling, memoization, slg_resolution, graphs, datalog]).
skill(prolog_testing,                [testing, unit_tests, plunit, assertions]).
skill(prolog_web_services,           [http, web_services, rest_api, json, websockets]).
skill(scryer_prolog_standards,       [scryer, modules, reif, si, chars, iso_purity]).
skill(swi_prolog_standards,          [swi, swipl, dicts, strings, packs, modules]).
skill(tau_prolog_standards,          [tau, javascript, dom, browser, nodejs]).
skill(trealla_prolog_standards,      [trealla, wasm, embedded, fast_parsing]).

%% skill_path(?SkillName:atom, ?RelativePath:chars) is nondet.
%  Relative path to the skill's SKILL.md definition file.
skill_path(prolog_conventions,            ".agents/skills/prolog-conventions/SKILL.md").
skill_path(prolog_code_review,            ".agents/skills/prolog-code-review/SKILL.md").
skill_path(prolog_clp_constraints,        ".agents/skills/prolog-clp-constraints/SKILL.md").
skill_path(prolog_dcg_mastery,            ".agents/skills/prolog-dcg-mastery/SKILL.md").
skill_path(prolog_debugging_workflow,     ".agents/skills/prolog-debugging-workflow/SKILL.md").
skill_path(prolog_declarative_workflow,   ".agents/skills/prolog-declarative-workflow/SKILL.md").
skill_path(prolog_engine_onboarding,      ".agents/skills/prolog-engine-onboarding/SKILL.md").
skill_path(prolog_ffi_wasm_embedding,     ".agents/skills/prolog-ffi-wasm-embedding/SKILL.md").
skill_path(prolog_initializer,            ".agents/skills/prolog-initializer/SKILL.md").
skill_path(prolog_library_discovery,      ".agents/skills/prolog-library-discovery/SKILL.md").
skill_path(prolog_linter_static_analysis, ".agents/skills/prolog-linter-static-analysis/SKILL.md").
skill_path(prolog_migrate_project,        ".agents/skills/prolog-migrate-project/SKILL.md").
skill_path(prolog_neurosymbolic_agent,    ".agents/skills/prolog-neurosymbolic-agent/SKILL.md").
skill_path(prolog_packaging,              ".agents/skills/prolog-packaging/SKILL.md").
skill_path(prolog_performance_profiling,  ".agents/skills/prolog-performance-profiling/SKILL.md").
skill_path(prolog_release,                ".agents/skills/prolog-release/SKILL.md").
skill_path(prolog_tabling,                ".agents/skills/prolog-tabling/SKILL.md").
skill_path(prolog_testing,                ".agents/skills/prolog-testing/SKILL.md").
skill_path(prolog_web_services,           ".agents/skills/prolog-web-services/SKILL.md").
skill_path(scryer_prolog_standards,       ".agents/skills/scryer-prolog-standards/SKILL.md").
skill_path(swi_prolog_standards,          ".agents/skills/swi-prolog-standards/SKILL.md").
skill_path(tau_prolog_standards,          ".agents/skills/tau-prolog-standards/SKILL.md").
skill_path(trealla_prolog_standards,      ".agents/skills/trealla-prolog-standards/SKILL.md").

%% skill_capability(?SkillName:atom, ?Capability:atom) is nondet.
skill_capability(SkillName, Cap) :-
    skill(SkillName, Caps),
    member(Cap, Caps).

%% find_skills_by_capability(+Capability:atom, -Skills:list(atom)) is det.
find_skills_by_capability(Cap, Skills) :-
    findall(Skill, skill_capability(Skill, Cap), Skills).
