Prefer prolog code with [logical purity properties](purity.md) ([Metalevel.at source](https://www.metalevel.at/prolog/purity)). Included in this are:
- prefer if_ and the predicates from reif.
- prefer clpz and clpb over impure built in predicates.
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

When relating condition to a value, then doing something further with that value, prefer an approach that isolates the test<->value relation. i.e. if_(G,A="A",A="B"), write(A) rather than writing A in each branch.

### Higher-Order Programming (`call/N`, `call//N`, `library(lambda)`)

Prefer higher-order predicates and closures over duplicating predicate clauses or DCG rules merely to change a sub-predicate or condition:

- **Higher-Order Predicates**: Use `call/N`, `maplist/N`, `foldl/N`, `include/3`, and `exclude/3` to process collections declaratively.
- **Higher-Order DCGs (`call//N`)**: Parameterize DCG rules with closures or non-terminals using `call//N` (e.g. `call(Goal, Arg)` inside `-->`) to avoid writing duplicate grammar traversals.
- **Lambda Expressions (`library(lambda)`)**: Use `:- use_module(library(lambda)).` and lambda abstractions (`\X^...`, `\X^Y^Goal`) for inline transformations, filtering, and mapping without creating single-use helper predicates.

### Use Term & Goal Expansion to Avoid Code Duplication

Leverage Prolog's compile-time expansion hooks (`user:term_expansion/2` and `user:goal_expansion/2`) to eliminate repetitive code structures, redundant clause boilerplate, or macro-like patterns instead of duplicating logic across multiple rules.

- **`term_expansion/2`**: Use to transform whole clauses or generate families of predicates at compile time (e.g., generating getter/setter clauses, enum mappings, or boilerplate wrapper rules).
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
- **Early Pruning**: Place deterministic, non-suspending, and always-terminating goals (such as `dif/2` and CLP(Z) constraints) before general search goals to prune the search space early.
- **Engine Delegation**: Delegate searching, backtracking, and indexing tasks to the Prolog engine rather than building manual search/indexing loops in Prolog code.

Use logging for diagnostics meant to be left in and activated at runtime.

See the guidelines in [Covington](covington_style.md).

