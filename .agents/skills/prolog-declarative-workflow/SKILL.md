---
name: prolog-declarative-workflow
description: Guidelines for AI-assisted Prolog development. Use declarative reasoning, explicit mode/determinism annotations, test-driven scaffolding, DCG structure generation, and choice-point audits.
---

# Declarative Prolog AI Workflow

Use this skill when designing, writing, refactoring, or auditing Prolog code with AI assistants.

## 1. Declarative Reasoning Directive
> **Core Principle**: Do not use imperative reasoning. Use declarative reasoning based on unification, logical constraints, and backtracking.

LLMs naturally default to imperative thinking (treating Prolog like Python or JavaScript). Force declarative mode by focusing on **relations, AST constructors, invariants, and unification patterns**.

---

## 2. Mode, Determinism & Choice-Point Contracts

Always annotate or specify predicate operational semantics:

- **Mode Annotations**: Indicate input (`+`) vs output (`-`) vs instantiated/uninstantiated (`?`) arguments.
- **Determinism Contracts**:
  - `det`: Exactly one solution; leaves no choice points.
  - `semidet`: Zero or one solution; fails cleanly without leaving unwanted choice points.
  - `multi`: At least one solution; supports backtracking enumeration.
  - `nondet`: Zero or more solutions.
- **Choice-Point Audits**: Ask the AI to audit predicates for unintended choice points, tail-recursion, and clean failure on invalid input.

---

## 3. Test-First Scaffolding Workflow

Write test assertions (`testing.pl` or `plunit`) *before* implementing or refactoring complex logic:

```prolog
:- use_module(library(testing)).

test(parse_literal) :-
    phrase(regex_ast(AST), "abc"),
    AST == lit("abc").

test(parse_kleene) :-
    phrase(regex_ast(AST), "a*"),
    AST == star(lit("a")).
```

Prompt the assistant with the test harness and ask it to generate the DCG or predicate clauses satisfying the tests.

---

## 4. Structuring DCGs & AST Constructors

AI excels at generating structural boilerplate for DCGs and AST trees when provided with data type constructors and grammar rules:

1. Provide AST term structures (e.g. `lit(Chars)`, `seq(R1, R2)`, `star(R)`).
2. Specify grammar production rules.
3. Request the DCG skeleton producing the AST.

---

## 5. Refactoring & Code Transformation

Use AI assistants for targeted declarative refactoring:
- Convert cut-heavy (`!`) code into pure logical forms (`dif/2`, `if_/3`, `clpz`).
- Audit and eliminate unnecessary choice points (`semidet` / `det` verification).
- Reorganize clauses into clean modules and add type/mode comments.
- Verify reversibility (ensuring predicates work bidirectionally when appropriate).
