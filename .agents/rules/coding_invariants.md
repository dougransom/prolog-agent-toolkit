# Core Prolog Coding Invariants

> **System Authority**: This document defines the permanent, non-negotiable coding invariants for all Prolog code within this project.
> These rules are persistently active for all AI agents and developers, independent of on-demand skill discovery.

## 1. Text & Strings as Character Lists (`chars`)
- **Strings are character lists**: Text and string data MUST be represented as lists of characters (`chars`).
- **Double quotes**: `double_quotes` MUST always be set to `chars`.
- **Prohibited**: Never use engine-specific string types, SWI dicts, or atomic strings for textual manipulation in portable code.

## 2. Logical Purity & Sound Term Inequality (`dif/2`, `dif/3`, `if_/3`)
- **Purity First**: Write pure, declarative relations that preserve bidirectionality and work in all argument modes (`+`, `-`, `?`).
- **No Impurity for Performance**: NEVER introduce cuts (`!`), negation-as-failure (`\+/1`), or soft cuts (`->`) merely for performance optimization.
- **Mandatory Justification for Correctness**: If an impure construct (`!`, `\+/1`, or `->`) must be introduced for *correctness* when pure logic constructs (`if_/3`, `dif/2`) cannot express the relation, write an explicit inline comment explaining precisely why pure constructs were insufficient.
- **Sound Inequality**: Always prefer `dif(X, Y)` over `\+ (X = Y)` or `X \= Y`. Use `dif(X, Y, Truth)` to reify term inequality into boolean `Truth`.

## 3. Direct Reification & `cond_t` (DRY Principle)
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

## 4. Safe Monotonic Type Testing
- **Prefer Safe Type Tests**: Use monotonic type tests from `library(si)` (`list_si/1`, `atom_si/1`, `chars_si/1`, `integer_si/1`) that safely suspend or fail monotonically on uninstantiated variables.
- **Prohibited**: Never use non-monotonic, unsafe type tests such as `is_list/1`.

## 5. Clean vs. Defaulty Data Representations
- **Functor Discrimination**: Represent composite terms using distinct principal functors for each case (e.g. `leaf(V)` vs. `node(Left, Right)`).
- **Avoid Defaulty Structures**: Avoid data structures that require runtime `var/1`/`nonvar/1` testing or catch-all default clauses to discern structure. Convert raw inputs into clean trees at domain boundaries.

## 6. Meaningful & Idiomatic Variable Naming
- **Public & Non-Trivial Clauses**: Use domain-descriptive variable names (`Tree`, `TokenStream`, `Result`, `Acc`) instead of arbitrary placeholders (`Arg1`, `P2`).
- **Local Tight Traversals**: Short, standard names (`X`, `Y`, `Xs`, `Ys`, `N`) are encouraged in tight list traversals, CLP constraints, and local closures.
- **Dual-Mode Predicates**: Clarify parameter roles for dual-mode predicates (e.g. `InputOrMatch`, `RestOrState`).
- **Threaded Pairs**: Use consistent naming for threaded state pairs (`L0, L1, ..., L` for character streams; `S0, S1, ..., S` for accumulators).

## 7. ISO DCG Indicator Convention (`Name//Arity`)
- **Non-Terminal Notation**: Always use `Name//Arity` notation (e.g. `parse_item//1`) for DCG non-terminals in:
  - Module export lists: `:- module(my_module, [parse_item//1]).`
  - Module import lists: `:- use_module(my_module, [parse_item//1]).`
  - Covington documentation headers: `%% parse_item//1`

## 8. Meta-Predicate Declarations (`meta_predicate`)
- **Mandatory Declarations**: When defining module-level predicates that accept callable goals (`0`), closures (`1`..`N`), DCG non-terminals (`//` or `2`), or module-sensitive terms (`:`), always insert explicit `:- meta_predicate` declarations directly below the module header.
- **Exact Arity Specification**: Specify exact closure arities for higher-order arguments (e.g. `2` for a closure taking 2 extra arguments) and standard specifiers (`+`, `-`, `?`, `*`) for non-callable data arguments. Never declare data arguments as `:` or `0`.
