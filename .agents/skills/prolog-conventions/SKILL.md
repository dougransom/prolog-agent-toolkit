---
name: prolog-conventions
description: Coding standards and guidelines for writing portable ISO-compliant Prolog code across Prolog systems. Use when writing code intended to run across multiple engines subject to engine capabilities.
---

# Portable ISO Prolog Conventions

## Universal Library Coding Standards vs Engine Loading

The programming standards, purity principles, and predicate usage guidelines documented across standard library capabilities — including:
- **Reified Logic & Conditionals**: `=(X, Y, Truth)`, `cond_t/3`, `if_/3`, `dif/2`, `memberd_t/3`
- **Integer Constraints**: `CLP(Z)` / `CLP(FD)` (`#=`, `label/1`, `labeling/2`)
- **Definite Clause Grammars**: pure DCG syntax (`-->`), `call//N`, ISO `Name//Arity` indicators
- **Character I/O & Strings**: double-quoted character lists (`chars`)
- **Safe Monotonic Type Testing**: `library(si)` (`list_si/1`, `integer_si/1`, `chars_si/1`)
- **Higher-Order Programming**: `call/N`, closures, `library(lambda)` / `yall`
- **Formatted Output & Utilities**: `format/2..3`, `library(lists)`, `library(assoc)`, `library(between)`

are **universal Prolog coding standards** for ANY Prolog engine supporting those capabilities.

While the module loading directive (e.g. `:- use_module(library(clpz)).` in Scryer/Trealla vs `:- use_module(library(clpfd)).` in SWI) may be dialect-specific or idiosyncratic to a particular engine, dialect skills document that loading header while referencing these universal Prolog coding standards for code style, purity, and predicate contracts.

## Core Guidelines

1. **Logical Purity & Term Inequality (`dif/2`, `dif/3`)**: Prefer pure predicates (`dif/2`, `dif/3`, `if_/3`). NEVER introduce cuts (`!`), negation-as-failure (`\+/1`), or soft cuts (`->`) for performance optimization. If an impure construct (`!`, `\+/1`, `->`) must be introduced for *correctness* (when pure constructs `if_/3` or `dif/2` cannot express the logic), write an explicit inline comment justifying why pure logic constructs were insufficient.
   - Prefer `dif(X, Y)` over `\+ (X = Y)` for sound term inequality constraints.
   - Use `dif(X, Y, Truth)` to reify term inequality into boolean `Truth` (`true` when terms are different, `false` when unified).
   - Pass partial closure `dif(Val)` to `tfilter/3` for pure higher-order list filtering:
     ```prolog
     % Remove all occurrences of 'a' deterministically without cuts
     remove_a(List, Filtered) :-
         tfilter(dif(a), List, Filtered).
     ```
2. **Strings as Character Lists (`chars`)**: Represent strings and text as lists of characters (`chars`). `double_quotes` must always be set to `chars`.
3. **Safe Type Testing**: Prefer pure, safe type tests (e.g. `library(si)`: `list_si/1`, `atom_si/1`, `chars_si/1`, `integer_si/1`) over impure non-monotonic type checks (`is_list/1`).
4. **Descriptive & Idiomatic Variable Naming**: Prefer meaningful, domain-descriptive names (`Tree`, `TokenStream`, `Result`, `Acc`) for public predicate parameters and complex clauses, avoiding arbitrary placeholders (`Arg1`, `P2`). Short, standard names (`X`, `Y`, `Xs`, `Ys`, `N`) remain encouraged in tight list traversals, mathematical constraints, and local closures. For dual-mode/polymorphic predicates, use clear parameter names (`InputOrMatch`, `RestOrState`). Use `L0, L1, ..., L` for character stream pairs and `S0, S1, ..., S` for state accumulator pairs.
5. **Direct Reification & `cond_t` (DRY Principle)**: Prefer direct reified predicates (`=(X, Y, Truth)`, `memberd_t/3`, `dif/3`) over wrapping boolean assignments inside `if_/3`. Aggressively prefer `cond_t` over `if_` and `->` when selecting between choices or values to avoid repeating target variable assignments across true and false branches (Don't Repeat Yourself principle).
6. **Higher-Order Logic, Lambdas & Reified Traversals (`tfilter/3`, `tpartition/4`)**: Prefer passing partial goals/closures to higher-order predicates (`call/N`, `maplist/N`, `foldl/N`, `tfilter/3`, `tpartition/4`) and `library(lambda)` (`\X^...`, `\X^Y^Goal`) over writing primitive recursive list traversals or non-reified `include/3`/`exclude/3`:
   ```prolog
   % Prefer maplist/N with partial goal closure over manual recursive loops
   double_item(X, Y) :- Y #= X * 2.
   double_all(Xs, Ys) :- maplist(double_item, Xs, Ys).

   % Pure reified list filtering and partitioning
   keep_zeros(Numbers, Zeros) :-
       tfilter((=)(0), Numbers, Zeros).

   partition_zeros(Numbers, Zeros, NonZeros) :-
       tpartition((=)(0), Numbers, Zeros, NonZeros).
   ```
7. **Standard & Higher-Order DCGs**: Use Definite Clause Grammars (`-->`) for sequence parsing, formatting, and tree transformations. Use `call//N` for higher-order DCG non-terminals. Always use ISO `Name//Arity` indicator notation (e.g. `parse_item//1`) in `:- module/2` export lists, `:- use_module/2` import lists, and Covington predicate doc headers:
   ```prolog
   :- module(my_parser, [
       parse_item//1  % Exports DCG non-terminal parse_item//1 (expands to parse_item/3)
   ]).

   % Parameterizing a DCG rule using call//N closure
   separated_by([], _) --> [].
   separated_by([X|Xs], Sep) -->
       call(Sep, X),
       separated_by(Xs, Sep).
   ```
8. **Explicit Library Declarations**: Always explicitly import required library modules (e.g. `:- use_module(library(dcgs)).`, `:- use_module(library(charsio)).`, `:- use_module(library(lambda)).`, `:- use_module(library(clpz)).`). Do not assume SWI-style autoloading when targeting ISO or embedded engines.
9. **Control Structures & CLP(Z) Constraints**: Use standard ISO control structures `(,)/2`, `(;)/2`. Prefer CLP(Z) constraints (`#=`, `#>`, `all_distinct/1`) and reified arithmetic (`zcompare/3`, `'#='(X, Y, Truth)`, `clpz_t/2`) over low-level evaluation (`is/2`, `>/2`). Always post domain declarations (`ins`, `in`) before posting complex relations to enable early constraint propagation. Link model flags via `#<==>` (e.g. `X #> 10 #<==> B #= 1`) and pass partial closures `(#<)(0)` to `tfilter/3`.
10. **Coroutining & Goal Suspension**: Use `freeze/2` for single-variable activation guards (`nonvar/1`) and `when/2` for multi-variable or disjunctive activation conditions (`(nonvar(A) ; nonvar(B))`). Prefer CLP(Z)/`dif/2` over manual coroutining where domain-specific constraints apply.
11. **Clean Data Representations**: Prefer clean data structures where element kinds are distinguished by principal functor (`leaf(L)` vs `node(L, R)`). Avoid defaulty representations that force runtime type tests (`var/1`) or procedural default branches. Convert raw input data into clean trees early.
12. **Macro & Compile-Time Expansion**: Use Prolog's macro mechanism (`user:term_expansion/2` and `user:goal_expansion/2`) to transform clauses or rewrite inline goals at compile time to eliminate boilerplate and redundant rules. Prefer static compile-time expansion over dynamic database modification (`asserta`/`assertz`).
13. **Avoid Non-Standard Extensions**: Do not rely on engine-specific types (e.g. SWI dicts or SWI string types) when writing standard Prolog code.
14. **Library Steering vs Reading Source**: Rely on dialect-specific Standard Library Cheat Sheets for module header declarations and predicate exports. AI assistants MUST NOT read raw standard library implementation source files, relying instead on concise cheat sheets and pre-trained semantics to save context tokens.
15. **Safety**: Execute code using `prolog-safe`.

16. **Prolog Tooling in Prolog (ISO Core + Engine Shims)**: Programs that parse, rewrite, transform, analyze, or generate Prolog source code SHOULD themselves be implemented in Prolog, exploiting the language's homoiconicity (code = terms = data). Structure such tools using an ISO-common core with flat, engine-specific shim files:
    - **ISO core** (`core.pl`): All term reading (`read_term/2`), DCG-based traversal and transformation, `copy_term/2`, `functor/3`, `=..`, and CLP(Z) constraints. This layer MUST NOT use engine-specific predicates or library paths.
    - **Flat shim files** (`scryer_shim.pl`, `swi_shim.pl`, `trealla_shim.pl`, etc.): Each shim defines only what differs per engine — module load paths, flag names, engine-specific built-ins — and exports a uniform interface consumed by the core.
    - **Entry point** (`run.pl`): Selects and loads the appropriate shim (e.g. via `PROLOG_ENGINE` flag or conditional compilation), then loads `core.pl`.
    ```
    tool/
      core.pl          % ISO common logic — read_term, DCG transforms, copy_term, CLP(Z)
      scryer_shim.pl   % Scryer-specific: library paths, flags, use_module headers
      swi_shim.pl      % SWI-specific: pack paths, string interop, module conventions
      trealla_shim.pl  % Trealla-specific: WASM bindings, standard library differences
      run.pl           % entry point: loads engine shim + core.pl
    ```
    This mirrors how Lisp macros process Lisp ASTs — the tool and the artifact share the same term language, so the full power of unification, DCGs, and constraints applies to the source being processed.

## Common ISO Punctuation & Syntax Diagnostics

| Invalid / Non-ISO Syntax | Correct ISO / Scryer Syntax | Fix Rationale |
| :--- | :--- | :--- |
| `// comment` or `# comment` | `% comment` | Prolog line comments MUST use `%` or `/* ... */` |
| `X != Y` | `dif(X, Y)` or `X \= Y` | C-style `!=` is invalid operator; use pure `dif/2` |
| `X <= Y` | `X #=< Y` or `X =< Y` | Less-than-or-equal operator is `=<` |
| `rule : body.` | `rule :- body.` | Rule neck operator is `:-` |
| `dcg_rule -> body.` | `dcg_rule --> body.` | DCG rule neck operator is `-->` |

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
- [Metalevel.at Clean Data Representations](https://www.metalevel.at/prolog/data#clean)
- [Metalevel.at Prolog Efficiency](https://www.metalevel.at/prolog/efficiency)

