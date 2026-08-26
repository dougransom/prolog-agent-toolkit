# Programmer Guidelines for AI-Assisted Prolog Development

When collaborating with AI coding assistants (Google Antigravity, Claude Code, Cursor, Copilot) on Prolog projects, follow these practical steering guidelines:

---

## 1. Provide Semantics & AST Shapes, Not Raw Logic Invention
LLMs struggle to invent complex Prolog relations from scratch, but excel at generating structural code when constrained by data types.
- **Do**: Provide AST term constructors (e.g., `lit(Chars)`, `seq(R1, R2)`), type invariants, and expected module structures.
- **Prompt Example**: *"Here are the constructors for my AST. Generate the DCG skeleton that produces this AST structure."*

---

## 2. Explicitly Specify Determinism & Mode Contracts
LLMs tend to generate cut-heavy or choice-point-polluted code unless explicitly instructed on operational semantics.
- **Specify Mode**: Indicate expected input (`+`) vs output (`-`) arguments.
- **Specify Determinism**: Tell the AI whether a predicate must be `det` (1 solution, no choice points), `semidet` (0 or 1 solution, fails cleanly), or `nondet` (supports backtracking).
- **Prompt Example**: *"Write this predicate to be semidet. It must fail cleanly on invalid input without leaving choice points."*

---

## 3. Use Test-First Prompting
Provide the test harness before requesting implementation code.
- **Do**: Write test cases (`testing.pl`, `plunit`, or test runner) first with expected inputs and outputs.
- **Prompt Example**: *"Here is my test harness (`test(parse_literal) :- phrase(regex(AST), "abc"), AST == lit("abc").`). Write the DCG rules satisfying these tests."*

---

## 4. Enforce the Declarative Mindset Directive
LLMs treat Prolog like "weird Python" by default. Flip the model into logic mode with explicit instructions:
- **Magic Prompt Directive**: *"Do not use imperative reasoning. Use declarative reasoning based on unification, constraints, and backtracking."*

---

## 5. Delegate DCG & Structural Boilerplate to AI
AI is exceptionally good at:
- Tokenizing and grammar production rules.
- DCG AST construction.
- Converting AST trees back into formatted text strings.

---

## 6. Use AI for Refactoring & Choice-Point Audits
Instead of asking AI to debug raw logic, ask targeted operational questions:
- *"List all choice points in this predicate."*
- *"Rewrite this cut-heavy (`!`) code using pure logical constructs (`dif/2`, `if_/3` from `library(reif)`)."*
- *"Rewrite this predicate to be tail-recursive."*
