# Logical Purity in Prolog

*Source: [Markus Triska - Logical Purity](https://www.metalevel.at/prolog/purity)*

At the heart of each great Prolog program is a property we call **logical purity** or simply **purity**. Informally, this means that the program has the properties we expect from a **relation**.

---

## 1. Intrinsic Definition

Purity can be defined inductively by referring to building blocks that guarantee purity by construction:

- `true/0` and `false/0` are pure.
- `(=)/2` and `dif/2` are pure.
- Arithmetic constraints like `(#=)/2`, `(#\=)/2` (CLP(FD)/CLP(Z)) are pure.
- `call(Goal)` is pure *iff* `Goal` is pure.
- `maplist(Goal, Ls)` is pure *iff* `Goal` is pure.
- `(A, B)` and `(A; B)` are pure *iff* `A` and `B` are pure.
- Reif predicates (`if_/3`, `tfilter/3`) are pure.

---

## 2. Extrinsic Definition

Purity can also be characterized by observable program properties from the outside:

- **No Side Effects**: If a goal produces output on the terminal (`write/1`, `format/2`) or modifies global state (`assertz/1`, `retract/1`), it is **not** pure.
- **Monotonicity**: Adding goals to a pure query can at most *reduce* the set of solutions, never increase it. If `(G, S=T)` succeeds unconditionally but `(S=T, G)` fails, `G` is non-monotonic and **not** pure.
- **Steadfastness**: A predicate is steadfast if its answers are independent of whether output arguments are instantiated before or after the call.
- **Purity Breakers**: Prominent constructs that break logical purity include cuts `!/0`, if-then-else `(->)/2`, `var/1`, `nonvar/1`, `==/2`, and database manipulation (`assertz/1`, `retract/1`).

---

## 3. Practical Importance of Pure Code

Pure Prolog code provides major advantages:

1. **Multi-directional execution**: Works in all directions (generators, checkers, query solvers).
2. **Reorderability**: Clauses and goals can be reordered freely without changing declarative meaning.
3. **Declarative Debugging**: Reasoning about code is simplified: adding constraints reduces solutions; removing constraints extends them.
4. **Thread Safety**: No destructive state updates, preventing data races in concurrent/web applications.
5. **Pure Testability**: Tests are simple queries that succeed or fail deterministically without needing terminal output capture.
