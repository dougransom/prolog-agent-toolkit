Prefer prolog code with [logical purity properties](purity.md) ([Metalevel.at source](https://www.metalevel.at/prolog/purity)). Included in this are:
- prefer `dif/2` over negation-as-failure `\+/1` (e.g. `dif(X, Y)` instead of `\+ (X = Y)`) for sound, pure term inequality.
- prefer `if_/3` and the predicates from `library(reif)`.
- **NEVER introduce cuts (`!`), negation-as-failure (`\+/1`), or soft cuts (`->`) for performance reasons.** Use pure efficiency techniques (first-argument indexing, `zcompare/3`, early constraint pruning) instead.
- **If cuts (`!`), `\+/1`, or `->` MUST be introduced for correctness instead of pure logic constructs, write an explicit comment in the code explaining why pure constructs (`if_/3`, `dif/2`) were insufficient.**
  ```prolog
  % CUT JUSTIFICATION [Correctness]: Impure cut used because stream I/O operations
  % cannot be reified with library(reif) and require side-effect commitment.
  read_token_cut(Stream, Token) :-
      get_char(Stream, Char),
      !,
      process_char(Char, Token).
  ```
- prefer CLP(Z) and CLP(B) over impure built-in predicates.
- prefer clean vs defaulty data representations ([Metalevel.at data#clean](https://www.metalevel.at/prolog/data#clean)).
- prefer pure efficiency techniques like argument indexing, reified `zcompare/3`, and early constraint pruning ([Metalevel.at efficiency](https://www.metalevel.at/prolog/efficiency)).



Use [Scryer Prolog](https://www.scryer.pl/) language and library documentation.
Tests use [Testing](https://github.com/bakaq/testing.pl).
Packages use [Bakage](https://github.com/bakaq/bakage).

Use any packages referenced in our project.

### Prefer DCGs for Simplification

Always look for opportunities to use Definite Clause Grammars (DCGs) when working with lists, sequences, strings (`chars`), or state threading. DCGs make code significantly simpler, more readable, and naturally pure by hiding implicit list accumulators.

- **Threading State or List Accumulation:** Replace manual `In`/`Out` pair parameters (e.g., `foo(X, L0, L)`) with a DCG rule (`foo(X) --> ...`).
- **Parsing & Tokenizing:** Use DCGs for text, string (`chars`), protocol, or AST parsing instead of string splitting or regex.
- **Generating & Formatting Text/Code:** Use DCGs for string building, serializing terms, or printing output instead of `append/3` chains or string concatenation.
- **Sequence Matching & Validation:** Use DCGs to inspect or match patterns over lists of any items without explicit head/tail destructuring.
- **ISO Indicator & Module Directives (`Name//Arity`):** Use `Name//Arity` (e.g. `parse_token//1`) in `:- module/2` export lists, `:- use_module/2` import lists, Covington comments (`%% rule//Arity`), and predicate identification.

When relating a condition to a value, then doing something further with that value, prefer an approach that isolates the test<->value relation (e.g. `if_(G, V = "A", V = "B"), write(V)` rather than writing `write/1` in each branch):

```prolog
% BAD: Duplicating side-effects inside branch goals
print_status(X) :-
    (   X = 0 -> write("zero")
    ;   write("non-zero")
    ).

% GOOD: Reify condition-to-value relation first, then perform action once
print_status(X) :-
    if_(X = 0, Status = "zero", Status = "non-zero"),
    write(Status).
```

### Prefer Direct Reified Predicates over Wrapping Booleans in `if_/3`

When working with `library(reif)`, always prefer direct reified predicates over wrapping boolean assignments inside `if_/3`:

- **Use Reified Equality (`=(X, Y, Truth)`)**: Use `=(X, Y, Truth)` (or `X = Y`) directly instead of `if_(X = Y, Truth = true, Truth = false)`.
- **Use Reified Predicates Directly**: Use reified predicates (e.g. `=/3`, `memberd_t/3`, `tpartition/4`) directly whenever a variable is being bound to boolean `true`/`false` based on a test.
- **Reserve `if_/3` for Non-Boolean Values & Control Flow**: Reserve `if_/3` strictly for selecting non-boolean values (`if_(G, Val = 'yes', Val = 'no')`) or executing conditional branches with different control paths.

```prolog
% BAD: Wrapping boolean assignment inside if_/3
is_zero_bool(X, Truth) :-
    if_(X = 0, Truth = true, Truth = false).

% GOOD: Use reified equality predicate directly
is_zero_bool(X, Truth) :-
    =(X, 0, Truth).
```

### Aggressively Prefer `cond_t` over `if_` / `->` (DRY Principle)

When choosing between two values or goals based on a test condition, aggressively prefer `cond_t` over `if_` or soft cuts (`->`):

- **Avoid Duplicating Target Variables (DRY Principle)**: In `if_(G, Val = 'yes', Val = 'no')`, the variable assignment `Val =` is repeated in both clauses. Prefer `cond_t` to isolate the condition and avoid repeating variable unification across branches.
- **Eliminate Soft Cuts (`->`)**: Replace procedural `(Condition -> Then ; Else)` with pure declarative `cond_t(Condition_1, Then, Else)`.

```prolog
% BAD: Repeating variable assignment in both branches of if_
status_name(Code, Status) :-
    if_(Code = 0, Status = "ok", Status = "error").

% GOOD: Aggressively use cond_t to specify condition and branches cleanly
status_name(Code, Status) :-
    cond_t(=(Code, 0), Status = "ok", Status = "error").
```

### Higher-Order Programming & Partial Goals (`call/N`, `call//N`, `library(lambda)`)

Prefer higher-order predicates and closures over primitive recursive list traversals or duplicating predicate clauses:

- **Prefer Partial Goals over Primitive Recursion**: Reuse higher-order predicates (`maplist/N`, `foldl/N`, `tfilter/3`, `include/3`, `exclude/3`) by passing partial goals/closures instead of writing manual recursive traversal loops.
  ```prolog
  % BAD: Primitive recursion duplicating traversal logic
  double_all([], []).
  double_all([X|Xs], [Y|Ys]) :-
      Y #= X * 2,
      double_all(Xs, Ys).

  % GOOD: Reuse maplist/N with a named partial goal predicate
  double_item(X, Y) :- Y #= X * 2.

  double_all(Xs, Ys) :-
      maplist(double_item, Xs, Ys).

  % GOOD (Lambda): Inline partial goal using library(lambda)
  double_all_lambda(Xs, Ys) :-
      maplist(\X^Y^(Y #= X * 2), Xs, Ys).
  ```
- **Higher-Order DCGs (`call//N`)**: Parameterize DCG rules with closures or non-terminals using `call//N` (e.g. `call(Goal, Arg)` inside `-->`) to avoid writing duplicate grammar traversals.
- **Lambda Expressions (`library(lambda)`)**: Use `:- use_module(library(lambda)).` and lambda abstractions (`\X^...`, `\X^Y^Goal`) for inline transformations, filtering, and mapping without creating single-use helper predicates.

### Meta-Predicate Declarations (`meta_predicate`)

When exporting or defining predicates inside a module that accept callable arguments (goals `0`, closures `1`..`N`, DCG rules `//` or `2`, dynamic goals `:`), always insert explicit `:- meta_predicate` declarations directly after the module header:

- **Module Name Expansion**: Tells the module system to resolve meta-arguments in the context of the *caller module* rather than the library module, preventing runtime `existence_error` exceptions.
- **Precise Arity Specifiers**:
  - `0`: 0-argument goal (executed with `call(Goal)` or direct evaluation).
  - `1`..`9`: Closures receiving $N$ additional arguments (e.g. `2` for `maplist/3`, `2` for `tfilter/3`, `3` for `foldl/4`).
  - `//` or `2`: DCG non-terminal closures expanded with difference lists.
  - `+`, `-`, `?`, `*`: Regular non-callable data arguments.
- **Avoid Anti-Patterns**: Never declare `meta_predicate` on pure data predicates, and never mark data arguments as `:` or `0` (which would force unintended caller-module term wrapping).

```prolog
:- module(my_higher_order, [
    custom_map/3,
    delimited//3
]).

:- meta_predicate
    custom_map(2, +, -),
    delimited(//, //, //, ?, ?).
```

### Use Term & Goal Expansion to Avoid Code Duplication

Leverage Prolog's compile-time expansion hooks (`user:term_expansion/2` and `user:goal_expansion/2`) to eliminate repetitive code structures, redundant clause boilerplate, or macro-like patterns instead of duplicating logic across multiple rules.

- **`term_expansion/2`**: Use to transform whole clauses or generate families of predicates at compile time (e.g., generating getter/setter clauses, enum mappings, or boilerplate wrapper rules).
  ```prolog
  % Example: Compile-time getter clause generation hook
  user:term_expansion(def_getter(Name, FieldIdx), (
      Goal :-
          arg(FieldIdx, Record, Val)
  )) :-
      Goal =.. [Name, Record, Val].
  ```
- **`goal_expansion/2`**: Use to rewrite specific inline goals before compilation (e.g., optimizing expressions, rewriting custom syntax shortcuts, or inserting compile-time instrumentation).
- **Static over Dynamic**: Prefer compile-time expansion (`term_expansion/2`) over dynamic runtime assertions (`asserta`/`assertz`) to maintain code clarity, static analysis, and compiler optimization properties.

### Mode, Determinism & Choice-Point Contracts

Always reason declaratively based on unification, constraints, and backtracking (never imperatively).

- **Mode Annotations**: Document arguments as input (`+`), output (`-`), or semi-instantiated (`?`) to clarify operational expectations.
- **Determinism Specification**:
  - `det`: Always succeeds with exactly 1 solution (no left-over choice points).
  - `semidet`: Succeeds 0 or 1 time; fails cleanly on invalid input without unwanted choice points.
  - `multi`/`nondet`: Explicitly intended for backtracking enumeration.
- **Choice-Point Audits**: Audit predicates to ensure cuts (`!`) are avoided where pure constructs (`if_/3`, `dif/2`, `clpz`) apply, and verify predicates fail cleanly when inputs violate contracts.

### Clean vs. Defaulty Data Representations

Always prefer **clean** data representations over **defaulty** ones ([Metalevel.at reference](https://www.metalevel.at/prolog/data#clean)):

- **Clean Definition**: A representation is *clean* if the kind of each component can be distinguished solely by its **principal functor** (e.g. `leaf(L)` vs `node(Left, Right)`).
- **Defaulty Anti-Pattern**: A representation is *defaulty* (a pun on "default" and "faulty") if elements cannot be distinguished by their principal functor (e.g., omitting `leaf/1` and using bare terms inside `node(L, R)`).
  ```prolog
  % BAD (Defaulty): Terms lack principal functors; forces var/1 checks and cuts
  eval(X, X) :- number(X), !.
  eval(add(A,B), Res) :- eval(A, VA), eval(B, VB), Res is VA + VB.

  % GOOD (Clean): Explicit principal functors leaf/1 vs node/2 allow pure indexing
  eval(num(N), N).
  eval(add(A, B), Res) :-
      eval(A, VA),
      eval(B, VB),
      Res #= VA + VB.
  ```
- **Why Defaulty is Harmful**:
  - Prevents automatic **argument indexing** (first-argument & JIT indexing).
  - Forces non-monotonic runtime type testing (e.g. `var/1`, `nonvar/1`, `compound/1`).
  - Requires procedural "default cases" and cuts (`!`) that destroy bidirectionality and multi-directional execution.
  - Prevents pattern matching on structural outlines (e.g. `node(leaf(_), leaf(_))`).
- **Boundary Conversion Strategy**: If receiving external unstructured or defaulty data (e.g. strings or dynamic terms), restrict impure type checks to a small boundary conversion predicate that converts defaulty terms into clean tagged compound terms *early*. "Prolog is brilliant with trees."

### Efficiency & Indexing Principles

Follow core Prolog efficiency principles ([Metalevel.at reference](https://www.metalevel.at/prolog/efficiency)):

- **"Pure things are fast, imperative things are slow"**: Pure declarative constructs allow compilers to apply argument indexing and tail-call optimization (TCO).
- **Argument Indexing**: Modern engines index on principal functors (especially the first argument). Placing distinguishing input parameters in the first argument position eliminates choice points automatically.
- **Reified Arithmetic Comparisons (`zcompare/3`)**: When conditional branches depend on integer comparisons, use `zcompare(Order, X, Y)` (from `library(clpz)`) to reify the comparison into an atom (`<`, `=`, `>`). Matching on the reified atom enables first-argument indexing and eliminates choice points without cuts.
  ```prolog
  % Reifies integer comparison into atom '<', '=', or '>' for first-argument indexing
  max_num(X, Y, Max) :-
      zcompare(Order, X, Y),
      max_num_(Order, X, Y, Max).

  max_num_(<, _, Y, Y).
  max_num_(=, X, _, X).
  max_num_(>, X, _, X).
  ```
- **Early Pruning**: Place deterministic, non-suspending, and always-terminating goals (such as `dif/2` and CLP(Z) constraints) before general search goals to prune the search space early.
- **Engine Delegation**: Delegate searching, backtracking, and indexing tasks to the Prolog engine rather than building manual search/indexing loops in Prolog code.

### Coroutining & Goal Suspension (`freeze/2`, `when/2`)

Use goal suspension to delay execution until arguments are sufficiently instantiated while preserving logical purity:

- **Constraint Primacy**: Always prefer dedicated declarative constraints (`CLP(Z)`, `dif/2`) over manual coroutining where applicable (e.g. `X #> 0` instead of `freeze(X, X > 0)`, or `dif(X, Y)` instead of `freeze(X, freeze(Y, X \== Y))`).
- **`freeze(Var, Goal)`**: Use when delaying a goal until a single variable is bound to a non-variable term (`nonvar(Var)`). Ideal for single-variable guards to prevent premature instantiation errors.
- **`when(Condition, Goal)`**: Use when activation depends on boolean conditions or multiple variables:
  - Disjunction: `when((nonvar(X) ; nonvar(Y)), Goal)` (triggers when either `X` or `Y` is bound).
  - Conjunction: `when((nonvar(X), nonvar(Y)), Goal)`.
  - Groundness: `when(ground(Term), Goal)`.

Use logging for diagnostics meant to be left in and activated at runtime.

See the guidelines in [Covington](covington_style.md).

