Prefer prolog code with [logical purity properties](purity.md) ([Metalevel.at source](https://www.metalevel.at/prolog/purity)). Included in this are:
- prefer if_ and the predicates from reif.
- prefer clpz and clpb over impure built in predicates.


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

Use logging for diagnostics meant to be left in and activated at runtime.

See the guidelines in [Covington](covington_style.md).
