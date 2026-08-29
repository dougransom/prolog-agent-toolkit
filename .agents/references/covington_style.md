---
@context: https://schema.org
@type: CreativeWork
name: "Prolog Coding Guidelines (Minimalist Full Edition)"
creator: "Michael A. Covington (concepts), distilled by Doug + Copilot"
description: "A complete but minimalist reinterpretation of Covington’s Prolog style principles for modern workflow and AI-assisted development."
version: "1.1"
license: "Public Domain"
---

> Note: This file is a Markdown reinterpretation of Covington’s PDF.  
> All ideas are preserved; wording is original.  
> Conversion performed intentionally for vibe‑coding workflow integration.

# Prolog Coding Guidelines (Minimalist Full Edition)

## 1. General Philosophy
- Write code for humans first, machines second.  
- Favor clarity over cleverness.  
- Make logical structure visible in the layout.  
- Keep predicates small and focused.  
- Prefer explicitness to implicit behavior.

---

## 2. File & Module Organization
- One major topic per file.  
- Export only the predicates meant for external use.  
- Provide a short module header describing purpose, key predicates, and assumptions.  
- Group related predicates together; avoid scattering definitions.

---

## 3. Predicate Naming
- Use lowercase_with_underscores for predicate names.  
- Names should describe *what* the predicate means, not how it works.  
- Boolean predicates should read like assertions (e.g., `is_sorted/1`).  
- Avoid overloaded names unless the meaning is identical.

---

## 4. Variable Naming
- Variables start with a capital letter.  
- Use meaningful names: `List`, `Tree`, `Result`, `Count`.  
- Use `_` or `_Var` for intentionally unused variables.  
- Avoid single-letter names except in tight, obvious contexts.

---

## 5. Clause Layout
- Keep each clause visually simple.  
- If the head is long, break after the `:-`.  
- Indent the body consistently (2–4 spaces).  
- Put each goal on its own line for readability.  
- Separate clauses with a blank line.

---

## 6. Goal Ordering
- Order goals by logical dependency: earlier goals should bind variables used later.  
- Place cheap tests before expensive ones.  
  ```prolog
  % BAD: Expensive graph traversal called before cheap type guard
  process_item(Item, Res) :-
      expensive_graph_search(Item, Res),
      integer(Item).

  % GOOD: Cheap guard test placed first to fail fast before expensive search
  process_item(Item, Res) :-
      integer(Item),
      expensive_graph_search(Item, Res).
  ```
- Place deterministic goals before nondeterministic ones when possible.  
- Avoid unnecessary choice points.

---

## 7. Cuts (`!`)
- Use cuts sparingly and intentionally.  
- A cut should signal a clear logical commitment.  
- Comment the purpose of each cut (“green cut”, “red cut”).  
- Prefer refactoring over relying on cuts for control flow.

---

## 8. Recursion & Iteration
- Prefer tail recursion when appropriate.  
- Keep accumulator variables clearly named (`Acc`, `Out`, `State`).  
  ```prolog
  % Tail-recursive sum using explicit accumulator parameter Acc
  list_sum(Ls, Sum) :-
      list_sum_(Ls, 0, Sum).

  list_sum_([], Acc, Acc).
  list_sum_([X|Xs], Acc0, Sum) :-
      Acc1 #= Acc0 + X,
      list_sum_(Xs, Acc1, Sum).
  ```
- Document the meaning of accumulators.  
- Avoid deeply nested recursion when a helper predicate improves clarity.

---

## 9. Pattern Matching
- Use pattern matching in the head when it improves clarity.  
- Avoid overly complex patterns in the head; move logic to the body if needed.  
- Prefer explicit matching to implicit unification buried in goals.

---

## 10. Data Structures
- Use lists for ordered collections.  
- Use structures (`foo(A,B,C)`) for well-defined records.  
- Document the shape of complex terms.  
- Avoid “mystery structures” with unclear argument meaning.

---

## 11. Comments & Documentation
- Comment *why*, not *what*.  
- Provide a short description above each predicate.  
- Document assumptions, invariants, and failure conditions.  
- Use `%` for single-line comments; avoid clutter.

---

## 12. Determinism & Modes
- Indicate expected modes in comments (`% foo(+List, -Result)`).  
- Ensure predicates behave consistently with their declared modes.  
- Avoid predicates that behave unpredictably depending on instantiation.

---

## 13. Error Handling
- Fail cleanly when appropriate.  
- Use explicit failure or exceptions when silent failure is misleading.  
- Document failure conditions.  
- Avoid relying on side effects to signal errors.

---

## 14. Efficiency Considerations
- Optimize only after correctness and clarity.  
- Use indexing-friendly clause ordering.  
- Avoid unnecessary backtracking.  
- Prefer deterministic helpers over nondeterministic general predicates.

---

## 15. Testing & Examples
- Provide small, clear examples in comments.  
- Include edge cases.  
- Keep examples minimal but representative.  
- Use them as living documentation.

---

## 16. Style Consistency
- Maintain consistent indentation, naming, and spacing.  
- Keep line lengths reasonable.  
- Use whitespace to group related ideas.  
- Let the code “breathe.”

---

## 17. Meta‑Predicates & Higher‑Order Code
- Use meta‑predicates (`maplist`, `include`, etc.) when they improve clarity.  
- Document the intent of higher‑order calls.  
- Avoid overly abstract meta‑programming unless necessary.

---

## 18. I/O & Side Effects
- Keep pure logic separate from I/O.  
- Document any predicate that performs side effects.  
- Avoid mixing computation and printing in the same predicate.

---

## 19. Debugging Practices
- Use tracing tools instead of adding temporary prints.  
- Keep debugging predicates separate from production code.  
- Document known failure points or tricky logic.

---

## 20. Final Notes
- Prefer simplicity.  
- Prefer readability.  
- Prefer explicit logic.  
- Let the structure of the problem guide the structure of the code.

---

Converted from Covington’s PDF into a minimalist, full‑coverage Markdown guide for vibe‑coding workflows.
