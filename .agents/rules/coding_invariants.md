# Core Prolog Coding Invariants

> **System Authority**: This document defines the permanent, non-negotiable coding invariants for all Prolog code within this project.
> These rules are persistently active for all AI agents and developers, independent of on-demand skill discovery.
> **Relationship to [codingstandards.md](../../codingstandards.md)**: This document is the compact, always-on baseline guardrail. For exhaustive syntax schemas, Covington layout, PlDoc mode/determinism contracts, CLP constraint modeling, and higher-order architecture patterns, AI agents and developers MUST consult [codingstandards.md](../../codingstandards.md).

## 1. Text & Strings as Character Lists (`chars`)
- **Strings are character lists**: Text and string data MUST be represented as lists of characters (`chars`).
- **Double quotes**: `double_quotes` MUST always be set to `chars`.
- **Prohibited**: Never use engine-specific string types, SWI dicts, or atomic strings for textual manipulation in portable code.

## 2. Logical Purity & Sound Term Inequality (`dif/2`, `dif/3`, `if_/3`, DCG Pushback Lists)
- **Purity First**: Write pure, declarative relations that preserve bidirectionality and work in all argument modes (`+`, `-`, `?`).
- **No Impurity for Performance or Lookahead**: NEVER introduce cuts (`!`), negation-as-failure (`\+/1`), or soft cuts (`->`) for performance or lookahead.
- **Pure Alternatives Preferred**:
  - For conditional branching: Always prefer `if_/3` or `cond_t`.
  - For DCG lookahead / token inspection: Always prefer **pure DCG pushback / semicontext lists** (`lookahead(T), [T] --> [T]`) over cuts (`!`) or soft cuts (`->`).
  - For code duplication and table generation: Aggressively use **compile-time macro expansion (`term_expansion/2`, `maplist/3`)** for DRY.
- **Mandatory Justification for Correctness**: If an impure construct (`!`, `\+/1`, or `->`) must be introduced for *correctness* when pure logic constructs (`if_/3`, `dif/2`, pushback lists) cannot express the relation, write an explicit inline comment explaining precisely why pure constructs were insufficient (e.g. `% Justification: foreign I/O boundary`).
- **Sound Inequality**: Always prefer `dif(X, Y)` over `\+ (X = Y)` or `X \= Y`. Use `dif(X, Y, Truth)` to reify term inequality into boolean `Truth`.

## 3. AI Agent Cognitive Traps: Why LLMs Default to `!`, `\+`, `->` and How to Overcome Them

> **Why AI Models Fall Back to Imperative Prolog (Context for Human & Machine Readers)**:
> 1. **The 1000:1 Historical Training Bias**: Over 99% of historical Prolog code on GitHub, in textbooks (1980–2010), Rosetta Code, and older university assignments was written prior to Ulrich Neumerkel's `library(reif)` (2014+) and ISO standardization. In those legacy corpora, `!`, `\+`, and `->` were ubiquitous workarounds for lack of first-class indexing or reification. LLM next-token probabilities naturally mirror this legacy distribution unless strictly instructed.
> 2. **Imperative Control Flow Transfer**: LLMs reason across multiple programming languages. Concepts like `if (cond) { A } else { B }` in Python, C, or Java map intuitively to `( Cond -> A ; B )` and `!`. But in Prolog, `->` and `!` are *destructive cuts* that commit to choices, discard choice points, and destroy bidirectionality across other argument modes.
> 3. **The 5 `if_/3` Compiler Traps**: When AI models attempt pure reification, they frequently hit one of five common compiler/macro errors, panic, and revert to `!` or `->`. Understanding and resolving these five patterns is essential:
>    - **Trap 1: Compound Goals in Condition**: `if_((A, B), Then, Else)` fails because `library(reif)` requires a single truth-reifying callable whose last argument receives the boolean atom (`A(..., Truth)`). The engine throws `existence_error(procedure, ','/3)`.
>      *Fix*: Nest the reified conditions: `if_(A, if_(B, Then, Else), Else)`.
>    - **Trap 2: DCG Macro Expansion**: Calling `if_/3` directly inside a DCG rule body (`phrase --> if_(C, T, E).`) causes the DCG preprocessor to add stream arguments to `if_`, expanding it to `if_/5` (`existence_error: if_/5`).
>      *Fix*: Wrap the call in curly braces: `{ if_(C, T, E) }`, or split into pure distinct DCG clauses with `dif/2`.
>    - **Trap 3: Arity Mismatch on Engine Builtins**: Calling `if_(char_type(C, lower), ...)` fails because `char_type/3` is not an engine-provided reified truth predicate.
>      *Fix*: Define a binary truth predicate (`char_type_lower_t(C, Truth) :- ...`) or use pure list membership (`memberd_t(C, LowerChars, T)`).
>    - **Trap 4: Partial Unification in `if_/3`**: Calling `if_(Rest = ['*'|_], ...)` fails during macro expansion because `=(Rest, ['*'|_], Truth)` cannot unify open list tails.
>      *Fix*: Match against clean functor structures, use separate clauses, or match `Rest = [C|Cs]` first and then test `if_(C = '*', ...)`.
>    - **Trap 5: Option / Map Lookup Fallbacks**: Trying `member(Key(Val), Options) -> ... ; Val = Default` introduces a destructive soft cut.
>      *Fix*: Implement a pure recursive helper:
>      ```prolog
>      lookup_option([], _, Default, Default).
>      lookup_option([Opt|Opts], Key, Default, Val) :-
>          Opt =.. [K, V],
>          if_(K = Key, Val = V, lookup_option(Opts, Key, Default, Val)).
>      ```

## 4. Mandatory Post-Generation Self-Audit Checklist
Before presenting or committing any generated Prolog code, every AI agent MUST perform this self-audit:
1. **Search for `!`**: Does the generated code contain any exclamation marks (`!`)?
   - If yes: Can it be replaced with `dif/2`, `if_/3`, or first-argument indexing?
   - If an impure cut is strictly required (e.g. legacy foreign FFI, OS side-effect, interactive CLI prompt), is there an explicit comment formatted as `% Justification: <reason>`?
2. **Search for `->`**: Does the generated code contain `->` (excluding DCG `-->`)?
   - If yes: Refactor to `if_(Cond_t, Then, Else)` or `cond_t(Cond_t, Target, Choices)`.
3. **Search for `\+`**: Is `\+` used to check inequality (`\+ (X = Y)` or `\+ X = Y`)?
   - If yes: Replace immediately with `dif(X, Y)`.
4. **Search for `member/2` in Conditions**: Is `member/2` used inside an if condition?
   - If yes: Replace with `memberd_t/3` from `library(reif)`.

## 5. Direct Reification & `cond_t` (DRY Principle)
- **Direct Reification over `if_/3` for Booleans**: Always prefer direct reified predicates (e.g. `=(X, Y, Truth)`, `memberd_t/3`, `dif/3`, `tpartition/4`) over wrapping boolean assignments inside `if_/3` (e.g. use `=(X, Y, Truth)` instead of `if_(X = Y, Truth = true, Truth = false)`). Reserve `if_/3` strictly for selecting non-boolean values or executing distinct control branches.
- **Prefer `cond_t` over `if_` / `->`**: Aggressively prefer `cond_t` over `if_` and `->` when selecting choices or values based on a condition to avoid repeating target variable assignments across branches (Don't Repeat Yourself principle).
- **Style for Conditionals**: When testing, then generating a value, and then using that value, prefer to test and generate the value in the condition and consume the value *after* the condition:
  ```prolog
  % Preferred (DRY, test & generate in condition, use after):
  if_(Condition_t, Val = "A", Val = "B"),
  format("Result is ~s~n", [Val])

  % Avoid (repeating the action across both branches):
  if_(Condition_t, format("Result is A~n", []), format("Result is B~n", []))
  ```

## 6. Safe Monotonic Type Testing
- **Prefer Safe Type Tests**: Use monotonic type tests from `library(si)` (`list_si/1`, `atom_si/1`, `chars_si/1`, `integer_si/1`) that safely suspend or fail monotonically on uninstantiated variables.
- **Prohibited**: Never use non-monotonic, unsafe type tests such as `is_list/1`.

## 7. Clean vs. Defaulty Data Representations
- **Functor Discrimination**: Represent composite terms using distinct principal functors for each case (e.g. `leaf(V)` vs. `node(Left, Right)`).
- **Avoid Defaulty Structures**: Avoid data structures that require runtime `var/1`/`nonvar/1` testing or catch-all default clauses to discern structure. Convert raw inputs into clean trees at domain boundaries.

## 8. Meaningful & Idiomatic Variable Naming
- **Public & Non-Trivial Clauses**: Use domain-descriptive variable names (`Tree`, `TokenStream`, `Result`, `Acc`) instead of arbitrary placeholders (`Arg1`, `P2`).
- **Local Tight Traversals**: Short, standard names (`X`, `Y`, `Xs`, `Ys`, `N`) are encouraged in tight list traversals, CLP constraints, and local closures.
- **Dual-Mode Predicates**: Clarify parameter roles for dual-mode predicates (e.g. `InputOrMatch`, `RestOrState`).
- **Threaded Pairs**: Use consistent naming for threaded state pairs (`L0, L1, ..., L` for character streams; `S0, S1, ..., S` for accumulators).

## 9. ISO DCG Indicator Convention (`Name//Arity`)
- **Non-Terminal Notation**: Always use `Name//Arity` notation (e.g. `parse_item//1`) for DCG non-terminals in:
  - Module export lists: `:- module(my_module, [parse_item//1]).`
  - Module import lists: `:- use_module(my_module, [parse_item//1]).`
  - Covington documentation headers: `%% parse_item//1`

## 10. Meta-Predicate Declarations (`meta_predicate`)
- **Mandatory Declarations**: When defining module-level predicates that accept callable goals (`0`), closures (`1`..`N`), DCG non-terminals (`//` or `2`), or module-sensitive terms (`:`), always insert explicit `:- meta_predicate` declarations directly below the module header.
- **Exact Arity Specification**: Specify exact closure arities for higher-order arguments (e.g. `2` for a closure taking 2 extra arguments) and standard specifiers (`+`, `-`, `?`, `*`) for non-callable data arguments. Never declare data arguments as `:` or `0`.

## 11. Aggressive Compile-Time Macro Expansion (`term_expansion/2`, `maplist/3`) for DRY
- **Aggressive Macro Generation for DRY**: Whenever generating repetitive boilerplate, clause families, lookup tables, operator maps, character escape sequences, opcode decoders, or grammar keyword tables, AI agents MUST generate compile-time macro expansions (`user:term_expansion/2` or `user:goal_expansion/2`) rather than duplicating code across multiple clauses.
- **Prefer Batch `maplist/3` over Repeated Sequential Macro Invocations**: When expanding collections, generate a single batch collection macro (`maplist(ExpandItem, List, Clauses)`) rather than outputting repeated top-level single-item invocations (`f(x1). f(x2). f(x3). ...`).
- **Example Pattern**:
  ```prolog
  % Preferred (Option C Batch Collection Macro):
  user:term_expansion(keywords(Kws), Clauses) :-
      maplist(\Kw^(keyword(Kw) --> Chars)^(atom_chars(Kw, Chars)), Kws, Clauses).

  keywords([if, then, else, while, for, in, return]).

  % Avoid (Repeated boilerplate declarations):
  keyword(if)   --> "if".
  keyword(then) --> "then".
  keyword(else) --> "else".
  ```
- **Pure Lookahead & Pushback in DCGs**: When parsing ambiguous prefixes or inspecting lookahead tokens without consuming them, ALWAYS use pure DCG pushback lists (`lookahead(T), [T] --> [T]`) rather than cuts (`!`) or soft cuts (`->`).

