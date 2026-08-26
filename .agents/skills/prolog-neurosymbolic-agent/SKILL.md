---
name: prolog-neurosymbolic-agent
description: Architecture guidelines for Neurosymbolic AI workflows integrating LLMs with Prolog constraint engines. Use when combining natural language processing with formal logical verification, ground-truth checking, and rule-based reasoning.
---

# Neurosymbolic AI & LLM + Prolog Architecture Guidelines

Use this skill when designing neurosymbolic AI agents where an LLM handles natural language processing, semantic translation, or heuristic generation, while a Prolog engine serves as the deterministic logic solver, knowledge base, and safety verifier.

## 1. Division of Responsibility

```
                                  +------------------------------------+
                                  |            LLM Subagent            |
                                  | - Natural Language Parsing          |
                                  | - Heuristic Search Guidance        |
                                  | - User Explanation & Formatting    |
                                  +------------------------------------+
                                                    |
                                       Synthesizes  | Validates &
                                       AST/Facts    | Resolves Constraints
                                                    v
                                  +------------------------------------+
                                  |        Prolog Logic Engine         |
                                  | - Ground Truth Verification         |
                                  | - CLP(Z) Constraint Satisfaction   |
                                  | - Pure DCG AST Validation          |
                                  +------------------------------------+
```

---

## 2. Recommended Workflow Pattern

1. **LLM Translation Phase**: The LLM parses user requests into concrete Prolog facts or AST terms (e.g. `user_goal(Expr)`).
2. **Prolog Verification Phase**: Execute the goal in Prolog via `prolog-safe`. Prolog either:
   - Succeeds and returns ground-truth substitutions.
   - Fails deterministically, returning residual constraints or un-handled states.
3. **Feedback Loop**: If Prolog fails or detects invalid constraints, feed the Prolog error output directly back into the LLM context for automated self-correction.

---

## 3. Structural Invariants

- **Never Trust LLM Arithmetic or Logic**: Always delegate mathematical calculations, constraint checks, and recursive search to Prolog (`#=`, `library(clpz)`, pure DCGs).
- **Strict AST Schema**: Force the LLM to emit well-formed Prolog terms conforming to a predefined schema.
- **Safety Sandboxing**: Execute all LLM-generated Prolog code using safety runners (`scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`).
