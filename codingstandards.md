# Unified Prolog Coding Standards & Guidelines

> **Authority & Purpose**: This document is the standalone, authoritative coding standard for writing, refactoring, and reviewing Prolog code across both human programmers and AI/LLM assistants.  
> **Historical Lineage & Acknowledgements**: This standard builds upon and pays homage to the foundational work of Michael A. Covington et al. (*Coding Guidelines for Prolog*, 1994/2012), synthesizing classic Covington style principles (layout, readability, naming, modularity, and goal ordering) with modern declarative ISO Prolog practices (logical purity, reification, `chars`, pure DCGs, safe type testing, and CLP constraints).  
> **Scope & Applicability**: Standard ISO/IEC 13211-1 compliant code across Scryer Prolog, SWI-Prolog, Trealla Prolog, Tau Prolog, and GNU/Ciao Prolog systems.

---

## Table of Contents
1. [Core Philosophy & Principles](#1-core-philosophy--principles)
2. [Layout, Formatting & Visual Structure (Covington Standards)](#2-layout-formatting--visual-structure-covington-standards)
   - [2.1 The Principle of Visual Logical Structure](#21-the-principle-of-visual-logical-structure)
   - [2.2 Clause Layout & Indentation](#22-clause-layout--indentation)
   - [2.3 Punctuation, Commas & Line Spacing](#23-punctuation-commas--line-spacing)
   - [2.4 Predicate Contiguity & File Cohesion](#24-predicate-contiguity--file-cohesion)
3. [Naming Conventions](#3-naming-conventions)
   - [3.1 Predicate Naming & Semantics](#31-predicate-naming--semantics)
   - [3.2 ISO DCG Indicator Notation (`Name//Arity`)](#32-iso-dcg-indicator-notation-namearity)
   - [3.3 Variable Naming: Meaningful vs. Standard Short](#33-variable-naming-meaningful-vs-standard-short)
   - [3.4 Dual-Mode & Polymorphic Variables](#34-dual-mode--polymorphic-variables)
   - [3.5 Threaded Difference-Lists & Accumulators](#35-threaded-difference-lists--accumulators)
   - [3.6 Anonymous & Intentionally Unused Variables](#36-anonymous--intentionally-unused-variables)
4. [Comments, Documentation & Covington Headers](#4-comments-documentation--covington-headers)
   - [4.1 Comment *Why*, Not *What*](#41-comment-why-not-what)
   - [4.2 Standard Covington / PlDoc Header Structure](#42-standard-covington--pldoc-header-structure)
   - [4.3 Mode Specifiers](#43-mode-specifiers)
   - [4.4 Determinism Indicators](#44-determinism-indicators)
   - [4.5 Living Documentation: Executable & Illustrative Examples](#45-living-documentation-executable--illustrative-examples)
5. [Goal Ordering & Clause Organization](#5-goal-ordering--clause-organization)
   - [5.1 Logical Dependency & Variable Binding](#51-logical-dependency--variable-binding)
   - [5.2 Cheap Tests Before Expensive Operations (Guard Ordering)](#52-cheap-tests-before-expensive-operations-guard-ordering)
   - [5.3 Deterministic Goals Before Nondeterministic Goals](#53-deterministic-goals-before-nondeterministic-goals)
   - [5.4 Clause Indexing & Argument Ordering](#54-clause-indexing--argument-ordering)
   - [5.5 Tail-Recursion Accumulators & $O(1)$ Stack Space (TCO)](#55-tail-recursion-accumulators--o1-stack-space-tco)
   - [5.6 First-Argument Functor Indexing & Choice-Point Elimination](#56-first-argument-functor-indexing--choice-point-elimination)
6. [Logical Purity & Control Flow](#6-logical-purity--control-flow)
   - [6.1 The Purity Imperative](#61-the-purity-imperative)
   - [6.2 Sound Term Inequality (`dif/2`)](#62-sound-term-inequality-dif2)
   - [6.3 Pure Conditionals & Reification (`if_/3`, `cond_t`)](#63-pure-conditionals--reification-if_3-cond_t)
   - [6.4 DRY Conditional Value Generation](#64-dry-conditional-value-generation)
   - [6.5 Direct Reification for Booleans](#65-direct-reification-for-booleans)
   - [6.6 Cuts (`!`) & Mandatory Impurity Justifications](#66-cuts--mandatory-impurity-justifications)
   - [6.7 Higher-Order Loops vs. Primitive Recursion (DRY)](#67-higher-order-loops-vs-primitive-recursion-dry)
   - [6.8 Declarative Slicing & Failure-Slice Debugging (`false`)](#68-declarative-slicing--failure-slice-debugging-false)
7. [Modern Declarative Replacements for Legacy Built-ins (`clpz` & `reif`)](#7-modern-declarative-replacements-for-legacy-built-ins-clpz--reif)
   - [7.1 The Paradigm Shift: Declarative Relations vs. Procedural Built-ins](#71-the-paradigm-shift-declarative-relations-vs-procedural-built-ins)
   - [7.2 Arithmetic: Why Legacy `is/2` Fails Declarativity (The `A is 3` Counterexample)](#72-arithmetic-why-legacy-is2-fails-declarativity-the-a-is-3-counterexample)
   - [7.3 Complete Reified Toolkit (`library(reif)`): Side-by-Side Reference](#73-complete-reified-toolkit-libraryreif-side-by-side-reference)
   - [7.4 Legitimate Circumstances for Legacy Built-ins](#74-legitimate-circumstances-for-legacy-built-ins)
8. [Data Representation & Types](#8-data-representation--types)
   - [8.1 Clean vs. Defaulty Data Modeling](#81-clean-vs-defaulty-data-modeling)
   - [8.2 Strings as Character Lists (`chars`)](#82-strings-as-character-lists-chars)
   - [8.3 Safe Type Testing (`library(si)`)](#83-safe-type-testing-librarysi)
   - [8.4 ISO Standard Error Terms & Exception Hygiene (`error(Formal, Context)`)](#84-iso-standard-error-terms--exception-hygiene-errorformal-context)
   - [8.5 Attributed Variables (`library(atts)`) for Extensible Metadata](#85-attributed-variables-libraryatts-for-extensible-metadata)
   - [8.6 Standard `Key-Value` Pairs (`-`) & $O(N \log N)$ `keysort/2`](#86-standard-key-value-pairs---on-log-n-keysort2)
9. [Definite Clause Grammars (DCGs) & Parsing](#9-definite-clause-grammars-dcgs--parsing)
   - [9.1 Pure DCGs as the Primary Default](#91-pure-dcgs-as-the-primary-default)
   - [9.2 Purity & Prohibition of Cuts in DCGs](#92-purity--prohibition-of-cuts-in-dcgs)
   - [9.3 Pure Lookahead & Pushback (No Cuts in DCGs)](#93-pure-lookahead--pushback-no-cuts-in-dcgs)
   - [9.4 State Threading in DCGs](#94-state-threading-in-dcgs)
10. [State Management & Threading Architectures](#10-state-management--threading-architectures)
    - [10.1 The State Threading Challenge in Pure Logic](#101-the-state-threading-challenge-in-pure-logic)
    - [10.2 DCG Difference Lists as Implicit State Monads](#102-dcg-difference-lists-as-implicit-state-monads)
    - [10.3 Structured State / Builder Compound Terms](#103-structured-state--builder-compound-terms)
    - [10.4 Higher-Order State Folding (`foldl/N`)](#104-higher-order-state-folding-foldln)
    - [10.5 Macro & Term Expansion (`term_expansion/2`, `goal_expansion/2`)](#105-macro--term-expansion-term_expansion2-goal_expansion2)
    - [10.6 Pure Associative Dictionaries (`library(assoc)`)](#106-pure-associative-dictionaries-libraryassoc)
    - [10.7 Dynamic Predicates (`assertz`/`retract`) vs. Pure State: Architectural Boundaries](#107-dynamic-predicates-assertzretract-vs-pure-state-architectural-boundaries)
11. [Text Formatting, I/O & Separation of Concerns](#11-text-formatting-io--separation-of-concerns)
    - [11.1 Separation of Pure Computation from I/O](#111-separation-of-pure-computation-from-io)
    - [11.2 Unified Format Calls (One Call vs. Chained Calls)](#112-unified-format-calls-one-call-vs-chained-calls)
    - [11.3 Pure String Construction via `charsio` & DCGs](#113-pure-string-construction-via-charsio--dcgs)
12. [Declarative Constraint Systems (`CLP(Z)`, `CLP(B)`, `CLP(FD)`)](#12-declarative-constraint-systems-clpz-clpb-clpfd)
    - [12.1 The Declarative Constraint Advantage (Constrain-and-Generate)](#121-the-declarative-constraint-advantage-constrain-and-generate)
    - [12.2 Integer Constraints (`library(clpz)` / `library(clpfd)`)](#122-integer-constraints-libraryclpz--libraryclpfd)
    - [12.3 Boolean Constraints (`library(clpb)`)](#123-boolean-constraints-libraryclpb)
    - [12.4 Constraint System Selection Guide (`CLP(Z)` vs. `CLP(B)` vs. `library(reif)`)](#124-constraint-system-selection-guide-clpz-vs-clpb-vs-libraryreif)
    - [12.5 Separation of Modeling from Search (Labeling Strategies)](#125-separation-of-modeling-from-search-labeling-strategies)
    - [12.6 Reified Arithmetic Comparison (`zcompare/3`)](#126-reified-arithmetic-comparison-zcompare3)
13. [Module Architecture, Exports & Meta-Predicates](#13-module-architecture-exports--meta-predicates)
    - [13.1 Module Headers & Explicit Imports](#131-module-headers--explicit-imports)
    - [13.2 Meta-Predicate Declarations (`meta_predicate`)](#132-meta-predicate-declarations-meta_predicate)
    - [13.3 Homoiconicity & Term Representations](#133-homoiconicity--term-representations)
    - [13.4 Tabling / Memoization (SLG Resolution) for Cyclic Graphs & Transitive Closures](#134-tabling--memoization-slg-resolution-for-cyclic-graphs--transitive-closures)
    - [13.5 Homoiconic Meta-Interpreter Scaffolding (The `mi/1` Pattern)](#135-homoiconic-meta-interpreter-scaffolding-the-mi1-pattern)
14. [Execution Safety, Timeouts & Sandboxing](#14-execution-safety-timeouts--sandboxing)
    - [14.1 21-Second Default Timeout](#141-21-second-default-timeout)
    - [14.2 Fibonacci Continuation Progression (34s, 55s, 89s...)](#142-fibonacci-continuation-progression-34s-55s-89s)
    - [14.3 Mandatory Safety Wrappers](#143-mandatory-safety-wrappers)
15. [Anti-Patterns & Prohibited Constructs](#15-anti-patterns--prohibited-constructs)


---

## 1. Core Philosophy & Principles

1. **Write for Humans First, Machines Second**: Code is read far more often than it is written. Layout, naming, comments, and structure must maximize immediate visual comprehension for both human maintainers and AI assistants.
2. **Aim for Standard ISO Prolog**: Generate declarative code conforming to standard ISO/IEC 13211-1, portable across ISO-oriented Prolog systems (Scryer, Trealla, SWI, Tau, GNU, Ciao) subject to engine capabilities.
3. **Declarative Relations First**: Model problems as multi-directional logical relations using unification, constraints, and backtracking rather than imperative step-by-step algorithms.
4. **Logical Purity over Premature Optimization**: Never introduce imperative cuts (`!`), negation-as-failure (`\+`), or soft cuts (`->`) solely for performance. Pure constructs (`dif/2`, `if_/3`, first-argument indexing, CLP constraints) maintain bidirectionality and soundness.
5. **Separation of Pure Logic and Side Effects**: Computational logic and text parsing must remain pure and free from I/O side effects. I/O should be confined to thin boundary predicates.
6. **DRY (Don't Repeat Yourself)**: Eliminate repeated assignments and structure across conditional branches. Test and bind once, use throughout.

---

## 2. Layout, Formatting & Visual Structure (Covington Standards)

### 2.1 The Principle of Visual Logical Structure
The visual layout of Prolog source code should directly reflect its underlying logical structure:
- **Predicate boundary**: A predicate consists of one or more clauses. Clauses belonging to the same predicate must stay together.
- **Clause boundary**: Each clause begins with its head and neck `:-` on the first line.
- **Goal boundary**: Each goal in a clause body occupies its own line, indented cleanly.

### 2.2 Clause Layout & Indentation
- **Indentation**: Indent clause bodies consistently by 4 spaces (or 2–4 spaces consistently across the project). Do not use tabs.
- **Clause Head and Neck**: Place the clause head and neck (`:-` or `-->`) on the first line.
- **Long Heads**: If a clause head is too long to fit comfortably within an 80-character line, place arguments on indented lines, but keep `:-` at the end of the head definition or on a new line before the body goals.
- **One Goal per Line**: Every goal in a rule body must appear on its own line. Never bunch multiple goals onto a single line.
- **Closing Period**: Place the terminating period `.` immediately after the final goal (or on its own line if the final goal is a complex multi-line expression).

```prolog
% CORRECT: Clean, readable Covington layout
process_user_record(User, Config, Result) :-
    validate_user(User),
    lookup_config_defaults(Config, EffectiveConfig),
    apply_user_policy(User, EffectiveConfig, Result).

% INCORRECT: Bunched goals, poor visual structure
process_user_record(User, Config, Result) :- validate_user(User), lookup_config_defaults(Config, EffectiveConfig), apply_user_policy(User, EffectiveConfig, Result).
```

### 2.3 Punctuation, Commas & Line Spacing
- **Commas at End of Line**: Always place the goal-separating comma `,` at the end of the line, not at the beginning of the next line.
- **Spacing Around Functors and Operators**:
  - Do NOT put whitespace between a functor and its opening parenthesis: write `foo(A, B)`, NOT `foo (A, B)`.
  - Put a single space after each comma in argument lists: `member(X, [A, B, C])`.
  - Put spaces around arithmetic and constraint operators: `X #= Y + 1`, `dif(A, B)`.
- **Blank Lines Between Clauses**: Separate distinct clauses with a single blank line. Use two blank lines (or a section header comment) to separate different predicate definitions.

```prolog
% CORRECT: Commas at line ends, proper spacing, blank line separation
filter_positives([], []).

filter_positives([X|Xs], Ys) :-
    if_(X #> 0,
        Ys = [X|Rest],
        Ys = Rest),
    filter_positives(Xs, Rest).
```

### 2.4 Predicate Contiguity & File Cohesion
- **Contiguous Clauses**: All clauses of a predicate must be placed contiguously in the file. Never scatter clauses of the same predicate across different sections.
- **One Major Topic per File**: Each module/file should encapsulate a single coherent responsibility or domain concept (e.g. `json_parser.pl`, `graph_algorithms.pl`).

---

## 3. Naming Conventions

### 3.1 Predicate Naming & Semantics
- **Case**: Always use `snake_case` (lowercase letters and underscores) for predicate names.
- **Declarative Meaning**: Name predicates after *what relationship holds*, not what procedure to execute:
  - Prefer relationship nouns and descriptive verbs: `tree_member/2`, `list_sum/2`, `user_authorized/2`.
  - Avoid imperative procedural names like `do_sum/2`, `calculate/2`, or `run_step/3`.
- **Boolean & Classification Predicates**: Predicates that act as boolean tests or type guards should read like declarations: `is_sorted/1`, `valid_token/1`, `empty_tree/1`.
- **Avoid Overloading**: Do not use the same predicate name with different arities for completely unrelated purposes.

### 3.2 ISO DCG Indicator Notation (`Name//Arity`)
- When referring to DCG non-terminals in documentation, comments, module exports (`:- module(...)`), and import lists (`:- use_module(...)`), **always** use the standard ISO indicator notation `Name//Arity` (representing the non-terminal's logical argument count, distinct from the transformed predicate's `Arity + 2`).

```prolog
% In module export header:
:- module(token_parser, [
    identifier//1,
    whitespace//0,
    integer_literal//1
]).
```

### 3.3 Variable Naming: Meaningful vs. Standard Short
- **Case**: All variables begin with a capital letter (e.g. `Stream`, `Item`) or underscore (e.g. `_`, `_Rest`).
- **Domain-Meaningful Names**: For public exported predicates, complex relations, and non-trivial clauses, use descriptive domain names: `TokenStream`, `SyntaxTree`, `ConfigRecord`, `Result`.
- **Idiomatic Short Names in Local Contexts**: In tight list traversals, standard recursion, CLP arithmetic relations, and local lambda closures, short standard variable names are encouraged:
  - Lists and elements: `[X|Xs]`, `[Y|Ys]`, `[E|Es]`.
  - Numbers and counts: `N`, `M`, `Count`, `Index`.
  - Accumulators and bounds: `Acc0, Acc1, Acc`, `Min, Max`.

### 3.4 Dual-Mode & Polymorphic Variables
When a predicate accepts arguments that can operate in dual modes (e.g. direct lists vs. DCG difference-lists, or input terms vs. match patterns), use names that clarify both roles:
- `InputOrMatch`
- `RestOrState`
- `SourceOrList`

### 3.5 Threaded Difference-Lists & Accumulators
When threading state or character streams through sequential goals:
- **Character Streams / Difference Lists**: Use `L0, L1, L2, ..., L` (or `Chars0, Chars1, ..., Chars`).
- **State Accumulators**: Use `S0, S1, S2, ..., S` (or `State0, State1, ..., State`).
- **Tail-Recursive Accumulators**: Use `Acc0, Acc1, ..., Acc` in helper predicates.

```prolog
% Threaded state transformation
transform_pipeline(Input, Output) :-
    step_alpha(Input, S0),
    step_beta(S0, S1),
    step_gamma(S1, Output).
```

### 3.6 Anonymous & Intentionally Unused Variables
- **Anonymous Singleton**: Use `_` for variables whose value is completely ignored and irrelevant.
- **Named Ignored Variables**: When documentation value is gained by naming an unused parameter, prefix it with an underscore: `_UserId`, `_DefaultValue`.

---

## 4. Comments, Documentation & Covington Headers

### 4.1 Comment *Why*, Not *What*
- Explain *why* a predicate or rule exists, what domain invariants hold, what assumptions are made, and any failure conditions.
- Do not merely restate the Prolog syntax in English.

```prolog
% INCORRECT (Restates the code)
% Add X to Y to get Z
add(X, Y, Z) :- Z #= X + Y.

% CORRECT (Explains domain meaning, invariants, and modes)
%% add(+X, +Y, -Z) is det.
%  Declarative integer sum relation holding when Z is the sum of X and Y.
add(X, Y, Z) :- Z #= X + Y.
```

### 4.2 Standard Covington / PlDoc Header Structure
Precede every exported or significant internal predicate with a structured documentation comment:

```prolog
%% predicate_name(+Input, -Output, ?State) is det.
%% dcg_name(?ParsedItem)//2 is semidet.
%
%  High-level summary of what the relation expresses.
%  Detailed explanation of parameters, preconditions, and invariants.
%  
%  @param Input  The source data structure or token stream.
%  @param Output The transformed result term.
%  @param State  Accumulator state record.
```

### 4.3 Mode Specifiers
Document argument instantiation expectations using standard ISO/PlDoc mode indicators:
- `+` : **Instantiated (Input)** — The argument must be instantiated to a non-variable term at call time.
- `-` : **Uninstantiated (Output)** — The argument is unbound at call time and unified with the output upon success.
- `?` : **Partially Instantiated or Unbound** — The argument may be instantiated or a variable; predicate works multidirectionally.
- `@` : **Read-Only / Ground** — The argument is inspected but not modified or unified.
- `:` : **Meta-Argument** — The argument is a module-sensitive goal or closure.

### 4.4 Determinism Indicators
Declare the determinism contract of predicates in the header line:
- `is det` : **Deterministic** — Exactly one solution; succeeds without leaving choice points.
- `is semidet` : **Semideterministic** — At most one solution (succeeds or fails cleanly); no choice points left.
- `is nondet` : **Nondeterministic** — Zero or more solutions via backtracking.
- `is multi` : **Multiple Solutions** — At least one solution; may generate more on backtracking.
- `is error` : **Error** — Always raises an exception.

### 4.5 Living Documentation: Executable & Illustrative Examples
Include minimal, representative query examples directly in comments to illustrate typical usage and edge cases:

```prolog
%% format_duration(+Seconds, -FormattedChars) is det.
%  Formats a total duration in seconds into a human-readable HH:MM:SS string.
%  
%  Example:
%    ?- format_duration(3665, Cs).
%       Cs = "01:01:05".
```

---

## 5. Goal Ordering & Clause Organization

### 5.1 Logical Dependency & Variable Binding
Order goals so that variables are bound before they are consumed by goals that require instantiation:
- Place generators and binders before consumers.
- Ensure logical dependencies flow naturally from left to right.

### 5.2 Cheap Tests Before Expensive Operations (Guard Ordering)
Place cheap guard tests (type checks, length checks, fast constraint filters) before expensive recursive traversals, deep unification, or external I/O:

```prolog
% INCORRECT: Expensive search executes before cheap type verification
process_item(Item, Result) :-
    expensive_graph_traversal(Item, SubTree),
    atom_si(Item),
    transform_tree(SubTree, Result).

% CORRECT: Cheap guard test fails fast before expensive computation
process_item(Item, Result) :-
    atom_si(Item),
    expensive_graph_traversal(Item, SubTree),
    transform_tree(SubTree, Result).
```

### 5.3 Deterministic Goals Before Nondeterministic Goals
Place deterministic goals and constraints before goals that create choice points or branch into large search trees. This prunes unviable branches early and minimizes backtracking overhead.

302: ### 5.4 Clause Indexing & Argument Ordering
303: Prolog engines index clauses on the principal functor of the first argument (and sometimes secondary arguments).
304: - **First-Argument Distinctness**: Structure predicate clauses so that the first argument cleanly discriminates between base cases, distinct AST functors, or constructors:
305:   ```prolog
306:   eval(num(N), N).
307:   eval(add(A, B), Res) :- eval(A, VA), eval(B, VB), Res #= VA + VB.
308:   eval(neg(A), Res)    :- eval(A, VA), Res #= -VA.
309:   ```
310: 
311: ### 5.5 Tail-Recursion Accumulators & $O(1)$ Stack Space (TCO)
312: Prolog engines apply **Tail Call Optimization (TCO)** (also called Last Call Optimization or LCO) when the recursive goal is the final goal in the clause body and no choice points remain. This transforms recursive traversals into $O(1)$ stack space (constant memory consumption), equivalent to an imperative `while` loop.
313: 
314: - **Body Recursion ($O(N)$ Stack Memory)**: Recursive goals followed by trailing operations require the engine to allocate an environment stack frame for every element, risking stack exhaustion on large lists:
315:   ```prolog
316:   % INCORRECT (Body recursion: stack grows O(N) because + operation trails recursion)
317:   list_sum_naive([], 0).
318:   list_sum_naive([X|Xs], Sum) :-
319:       list_sum_naive(Xs, RestSum),
320:       Sum #= X + RestSum. % Operation after recursive call prevents TCO!
321:   ```
322: 
323: - **Tail-Recursive Accumulator Pattern ($O(1)$ Stack Memory)**: Thread an accumulator parameter (`Acc0 -> Acc1`) and compute the state update *before* the tail-recursive call:
324:   ```prolog
325:   % CORRECT (Tail recursion with accumulator: O(1) stack space via TCO)
326:   %% list_sum(+List, -Sum) is det.
327:   list_sum(List, Sum) :-
328:       list_sum(List, 0, Sum).
329: 
330:   list_sum([], Sum, Sum).
331:   list_sum([X|Xs], Acc0, Sum) :-
332:       Acc1 #= Acc0 + X,
333:       list_sum(Xs, Acc1, Sum).
334:   ```
335: 
336: - **Reversing Lists: $O(N)$ Accumulator vs. $O(N^2)$ Naive `append`**:
337:   ```prolog
338:   % Naive reverse: O(N^2) time due to append/3 at each step
339:   % Efficient accumulator reverse: O(N) time and O(1) stack frames
340:   %% list_reverse(+List, -Reversed) is det.
341:   list_reverse(List, Reversed) :-
342:       list_reverse(List, [], Reversed).
343: 
344:   list_reverse([], Acc, Acc).
345:   list_reverse([X|Xs], Acc, Reversed) :-
346:       list_reverse(Xs, [X|Acc], Reversed).
347:   ```
348: 
349: ### 5.6 First-Argument Functor Indexing & Choice-Point Elimination
350: Prolog engines build indexing hash tables and jump instructions based on the **principal functor of the first argument** (`Arg1`). When `Arg1` contains a distinct functor or atom in each clause, the engine jumps directly to the matching clause in $O(1)$ time and **commits without allocating choice-point records**.
351: 
352: 1. **Place Primary Discriminator as Argument 1**:
353:    ```prolog
354:    % INCORRECT (Unindexed: discriminator is in Argument 2; creates unwanted choicepoints)
355:    handle_event(Session, login(User), StateOut) :- ...
356:    handle_event(Session, logout, StateOut)       :- ...
357:    handle_event(Session, heartbeat, StateOut)    :- ...
358: 
359:    % CORRECT (Indexed on Argument 1: engine jumps in O(1) with zero choicepoint overhead)
360:    handle_event(login(User), Session, StateOut) :- ...
361:    handle_event(logout, Session, StateOut)       :- ...
362:    handle_event(heartbeat, Session, StateOut)    :- ...
363:    ```
364: 
365: 2. **Avoid Variable First Arguments in Multi-Clause Predicates**: If a clause has an unbound variable in its first argument, indexing fails for that clause, forcing the engine to retain a choice point and fall back to linear clause scanning.
366: 
367: ---
368: 
369: ## 6. Logical Purity & Control Flow

### 6.1 The Purity Imperative
Prolog programs should remain pure first-order logic formulas whenever possible. Impure control predicates (`!`, `\+`, `->`) destroy commutativity, prevent multidirectional query execution, and introduce insidious bugs when variables are unbound.

### 6.2 Sound Term Inequality (`dif/2`)
- **ALWAYS** use `dif(X, Y)` for term inequality.
- **NEVER** use `\+ X = Y`, `\==`, or `\=` for logical discrimination. Negation-as-failure `\+` unsoundly fails if variables are uninstantiated at test time.

```prolog
% INCORRECT (Unsound with unbound variables)
non_matching_pair(X, Y) :-
    X \= Y.

% CORRECT (Declaratively sound constraint)
non_matching_pair(X, Y) :-
    dif(X, Y).
```

### 6.3 Pure Conditionals & Reification (`if_/3`, `cond_t`)
- Prefer `if_/3` (from `library(reif)`) over `-> / ;` to retain full logical reversibility and search-space completeness.
- Use `cond_t/3` when selecting alternatives based on truth values without repeating code.

```prolog
% INCORRECT (Destroys alternate search paths with cut)
member_check(X, [X|_]) :- !.
member_check(X, [_|Xs]) :- member_check(X, Xs).

% CORRECT (Pure, sound reification)
member_check(X, List) :-
    memberd_t(X, List, true).
```

### 6.4 DRY Conditional Value Generation
When testing a condition to determine a value and subsequently using that value, **test and generate the value inside the condition branch**, and perform the shared action **once after the condition**.

```prolog
% INCORRECT (Violates DRY: repeated format action across branches)
describe_parity(N) :-
    if_(even_t(N),
        ( Label = "even", format("Parity: ~s~n", [Label]) ),
        ( Label = "odd",  format("Parity: ~s~n", [Label]) )).

% CORRECT (DRY: determine Label in condition, execute shared action once)
describe_parity(N) :-
    if_(even_t(N), Label = "even", Label = "odd"),
    format("Parity: ~s~n", [Label]).
```

### 6.5 Direct Reification for Booleans
Do not wrap boolean terms in `if_/3`. Use direct reified predicates:

```prolog
% INCORRECT (Redundant if_ wrapper)
is_equal(X, Y, Truth) :-
    if_(X = Y, Truth = true, Truth = false).

% CORRECT (Direct reification)
is_equal(X, Y, Truth) :-
    =(X, Y, Truth).
```

### 6.6 Cuts (`!`) & Mandatory Impurity Justifications
- **Avoid Cuts for Performance**: Cuts (`!`), soft cuts (`->`), and negation‑as‑failure (`\+`) should be used only in **extremely rare** cases, never solely for performance or choice‑point suppression. Markus Triska advises that cuts be employed only when a pure logical alternative cannot express the required semantics.
- **Mandatory Justification for Correctness**: If an impure construct (`!`, `->`, `\+`) is strictly required for correctness (e.g. low-level I/O commit, interface with side-effecting foreign APIs, or non-logical commit where pure reification cannot apply), write an explicit, prominent comment explaining precisely why pure alternatives (`dif/2`, `if_/3`, clause indexing) were insufficient.

```prolog
% ACCEPTABLE USE WITH MANDATORY COMMENT:
commit_external_transaction(Handle) :-
    send_hardware_packet(Handle),
    !, % CUT JUSTIFICATION: Hardware protocol requires irreversible commit; backtracking would duplicate side effects.
    log_commit_success(Handle).
```

### 6.7 Higher-Order Loops vs. Primitive Recursion (DRY)
In adherence to the **Don't Repeat Yourself (DRY)** principle, prefer higher-order predicate abstractions (`maplist/N`, `foldl/N`, `tfilter/3`, `tpartition/4`) over writing repetitive primitive recursion loops:

1. **Standard List Higher-Order Relations**:
   - `maplist/2..N`: Transforms or asserts relations element-wise across lists.
   - `foldl/4..N`: Pure state threading and accumulation over list elements.
   - `library(lambda)`: Construct inline closures (`\X^...`, `\X^Y^Goal`) to eliminate single-use auxiliary loop helpers.

2. **Custom Higher-Order Predicates for Domain Data Structures**:
   - When defining recursive or compound data structures (binary trees, AST nodes, graphs, symbol tables), **do NOT write ad-hoc primitive recursion for every query, transformation, or traversal**.
   - **Write a general higher-order mapping/folding predicate once** for that structure, export it with `meta_predicate` declarations, and reuse it everywhere across the module:

```prolog
% Definition of custom binary tree data structure:
% leaf(Value) | node(Value, Left, Right)

:- meta_predicate tree_map(2, +, -).
:- meta_predicate tree_fold(3, +, +, -).

%% tree_map(:Closure, +TreeIn, -TreeOut) is det.
%  Applies Closure to each value in TreeIn, producing TreeOut.
tree_map(Closure, leaf(V0), leaf(V)) :-
    call(Closure, V0, V).
tree_map(Closure, node(V0, L0, R0), node(V, L, R)) :-
    call(Closure, V0, V),
    tree_map(Closure, L0, L),
    tree_map(Closure, R0, R).

%% tree_fold(:Closure, +Tree, +Acc0, -AccOut) is det.
%  Folds Closure across tree values in-order.
tree_fold(Closure, leaf(V), Acc0, AccOut) :-
    call(Closure, V, Acc0, AccOut).
tree_fold(Closure, node(V, L, R), Acc0, AccOut) :-
    tree_fold(Closure, L, Acc0, Acc1),
    call(Closure, V, Acc1, Acc2),
    tree_fold(Closure, R, Acc2, AccOut).
```

3. **Reusing Structure Combinators across Applications**:
   - Once `tree_map/3` or `tree_fold/4` is defined, operations like incrementing all nodes, collecting tree values into a list, or computing sums become simple 1-line declarative goals:

```prolog
% CORRECT (DRY: Reusing tree_map and tree_fold with lambda expressions)
increment_tree(Tree0, TreeOut) :-
    tree_map(\X^Y^(Y #= X + 1), Tree0, TreeOut).

sum_tree(Tree, Sum) :-
    tree_fold(\V^Acc^Out^(Out #= Acc + V), Tree, 0, Sum).
```

### 6.8 Declarative Slicing & Failure-Slice Debugging (`false`)
In pure Prolog programs (programs devoid of cuts, impure side effects, and non-logical built-ins), non-termination, unexpected failures, and logical defects can be diagnosed using **declarative slicing** (pioneered by Ulrich Neumerkel).

1. **The Mathematical Invariant of Slicing**:
   - By inserting the goal `false` into clause bodies, you construct a *failure slice* (a generalized, reduced program).
   - If a failure slice still **fails to terminate** (loops forever) or **fails unexpectedly**, the bug is **guaranteed to reside exclusively within the remaining visible goals of that slice**. No modification to the sliced-away goals can ever fix the issue!
   - This property allows human programmers and AI assistants to isolate non-termination and logic bugs in seconds without manual trace stepping.

2. **Diagnosing Non-Termination via Failure Slices**:
   ```prolog
   % ORIGINAL PREDICATE (Loops on query ?- list_member(X, [1,2,3]), false.):
   list_member(X, [X|_Xs]).
   list_member(X, [_Y|Xs]) :-
       list_member(X, Xs),
       dif(X, 0).

   % FAILURE SLICE (Insert false to isolate the non-terminating loop):
   list_member(X, [X|_Xs]) :- false.
   list_member(X, [_Y|Xs]) :-
       list_member(X, Xs), false,
       dif(X, 0). % <-- Sliced away: completely irrelevant to the non-termination!
   ```

3. **Why Slicing Requires Logical Purity**:
   - If a program uses impure cuts (`!`), negation-as-failure (`\+`), or `-> / ;`, inserting `false` changes procedural control flow and alters cut scope, destroying the monotonicity required for failure slicing. Purity is what makes Prolog programs mathematically debuggable.

---

## 7. Modern Declarative Replacements for Legacy Built-ins (`clpz` & `reif`)

### 7.1 The Paradigm Shift: Declarative Relations vs. Procedural Built-ins
Historical Prolog systems provided procedural, mode-restricted built-ins (`is/2`, `==/2`, `\==/2`, `memberchk/2`, `include/3`, `->/2`) that required arguments to be fully instantiated at call time. If called with uninstantiated variables, these built-ins either fail silently, produce unsound answers, or throw runtime `instantiation_error` exceptions.

Modern ISO Prolog replaces procedural built-ins with **declarative constraints (`library(clpz)`)** and **reified truth predicates (`library(reif)`)**, guaranteeing that predicates behave as true mathematical relations that work in all query directions.

### 7.2 Arithmetic: Why Legacy `is/2` Fails Declarativity (The `A is 3` Counterexample)
Legacy arithmetic evaluation with `is/2` is strictly unidirectional and procedural:

```prolog
% THE COUNTEREXAMPLE:
?- A is 3.
   A = 3.         % Appears to work...

?- 3 is A + 1.
   error(instantiation_error, (is)/2).  % CRASHES: cannot run backwards!

% MODERN CLP(Z) ARITHMETIC:
?- 3 #= A + 1.
   A = 2.         % Deduces A bidirectionally without error.
```

#### Legacy Arithmetic vs. Modern Declarative Replacements (`library(clpz)`)

> **Note on Existing Codebases**: Decades of textbooks, tutorials, and legacy Prolog codebases (Prolog-84, Quintus, older SWI/SICStus) make pervasive use of `is/2`, `>/2`, `between/3`, and `succ/2`. When writing new code or refactoring legacy modules, systematically replace these procedural operators with `library(clpz)` constraints to achieve true mathematical bidirectionality.

| Legacy Arithmetic Operator | Modern Replacement (`clpz`) | Failure Mode in Legacy Code | Modern Declarative Advantage |
| :--- | :--- | :--- | :--- |
| `X is Expr` | `X #= Expr` | Throws `instantiation_error` if `Expr` has unbound variables | Bidirectional; solves for any variable in the equation |
| `X =:= Y` | `X #= Y` | Crashes if `X` or `Y` are not fully ground | Unifies numeric values and posts relational equality |
| `X =\= Y` | `X #\= Y` | Crashes on uninstantiated variables | Posts sound integer disequality constraint |
| `X > Y` | `X #> Y` | Crashes on uninstantiated variables | Prunes domain bounds without requiring immediate ground values |
| `X < Y` | `X #< Y` | Crashes on uninstantiated variables | Sound strict inequality constraint |
| `X >= Y` | `X #>= Y` | Crashes on uninstantiated variables | Sound non-strict upper/lower bound pruning |
| `X =< Y` | `X #=< Y` | Crashes on uninstantiated variables | Sound non-strict inequality constraint |
| `between(Low, High, X)` | `X in Low..High` | Fails or crashes if bounds are variables; imperative loop | Pure finite domain constraint; composable with other constraints |
| `succ(Prev, Next)` | `Next #= Prev + 1, Next #>= 1` | Ad-hoc non-negative helper; crashes on invalid modes | Pure mathematical equation |
| `plus(A, B, C)` | `C #= A + B` | Ad-hoc built-in with mode limitations | General declarative addition across all directions |
| `( X < Y -> ... ; X =:= Y -> ... ; X > Y -> ... )` | `zcompare(Order, X, Y), if_(Order = (<), ...)` | Impure nested cuts; fails if arguments are uninstantiated | Pure 3-way ternary comparison (`<`, `=`, `>`) via reification |

- **Why Avoid `is/2`, `>/2`, `</2`, `=:=/2`**:
  - `is/2` requires the entire right-hand expression to be fully ground.
  - Comparison operators (`>`, `<`, `=:=`, `=\=`) immediately crash on variables rather than delaying until bounds are known.
  - `library(clpz)` (`#=`, `#\=`, `#>`, `#<`, `#>=`, `#=<`, `in`, `zcompare/3`) posts declarative algebraic constraints that prune search spaces early, support infinite domains, and execute in all calling modes.

### 7.3 Complete Reified Toolkit (`library(reif)`): Side-by-Side Reference

The complete `library(reif)` export interface provides 11 declarative predicates that eliminate all procedural cuts, negation-as-failure, and soft-cuts:

| Legacy / Impure Construct | Modern Declarative Replacement (`reif`) | Description & Declarative Role |
| :--- | :--- | :--- |
| `( Cond -> Then ; Else )` | `if_(Cond_1, Then_0, Else_0)` | Pure conditional; retains alternate branches if condition is uninstantiated |
| `X == Y` / `X = Y` (in test) | `=(X, Y, Truth)` | Reified term equality (`true` if equal, `false` if `dif/2`) |
| `\+ X = Y` / `X \= Y` / `\==` | `dif(X, Y, Truth)` | Reified term inequality (`true` if `dif/2`, `false` if equal) |
| `( CondA, CondB )` (in test) | `','(CondA_1, CondB_1, Truth)` | Reified conjunction (**AND**) with pure short-circuiting |
| `( CondA ; CondB )` (in test) | `';'(CondA_1, CondB_1, Truth)` | Reified disjunction (**OR**) with pure short-circuiting |
| `( Cond -> Goal ; true )` | `cond_t(Cond_1, Goal_0, Truth)` | Reified conditional execution; executes `Goal_0` when `Cond_1` holds, binds `Truth` |
| `memberchk(X, List)` | `memberd_t(X, List, Truth)` | Reified deterministic membership; sound on partial lists without cuts |
| `member(X, List)` (with test)| `tmember(Closure_2, List)` | Pure existential search for an element satisfying `call(Closure_2, X, true)` |
| `\+ \+ (member(X, L), Test)`| `tmember_t(Closure_2, List, Truth)`| Reified existential satisfaction; `true` if any element satisfies closure, `false` otherwise |
| `include(Goal, List, Out)` | `tfilter(Closure_2, List, Out)` | Pure higher-order filtering with 2-argument reified closure `call(C_2, X, T)` |
| `partition(Goal, List, In, Out)` | `tpartition(Closure_2, List, In, Out)` | Pure list partitioning based on reified truth value `true`/`false` |

---

#### 1. Reified Term Equality & Inequality: `=(X, Y, Truth)` & `dif(X, Y, Truth)`
Posts a sound constraint on `Truth` without committing before terms are sufficiently instantiated:
```prolog
% INCORRECT (Legacy test with impure ==)
compare_keys(Key1, Key2, Match) :-
    ( Key1 == Key2 -> Match = same ; Match = different ).

% CORRECT (Pure reified equality)
compare_keys(Key1, Key2, Match) :-
    if_(=(Key1, Key2), Match = same, Match = different).
```

---

#### 2. Reified Conjunction (AND): `','/3` — When & How to Use
- **Problem**: In standard Prolog, `(A, B)` succeeds if both goals succeed. But in reified contexts (inside `if_/3` or `tfilter/3`), the condition argument must be a closure that accepts a boolean truth value `Truth`.
- **Mechanism**: `','(A_1, B_1, Truth)` evaluates `A_1`. If `false`, it short-circuits with `Truth = false` without evaluating `B_1`. If `true`, `Truth` becomes whatever `B_1` evaluates to. If uninstantiated, it explores both possibilities purely.
- **When to Use**: When a conditional branch or list filter requires **multiple simultaneous conditions** without nested `if_` calls:

```prolog
% INCORRECT (Nested if_ statements creating verbose staircase code)
check_eligible(User, Status) :-
    if_(is_active_t(User),
        if_(has_verified_email_t(User), Status = eligible, Status = ineligible),
        Status = ineligible).

% CORRECT (Reified Conjunction via ','/3)
check_eligible(User, Status) :-
    if_((is_active_t(User), has_verified_email_t(User)),
        Status = eligible,
        Status = ineligible).
```

---

#### 3. Reified Disjunction (OR): `';'/3` — When & How to Use
- **Problem**: Testing whether *either* condition holds using `(A ; B) -> Then ; Else` creates impure cuts and silently suppresses alternate valid bindings.
- **Mechanism**: `';'(A_1, B_1, Truth)` evaluates `A_1`. If `true`, it short-circuits with `Truth = true` without evaluating `B_1`. If `false`, `Truth` becomes whatever `B_1` evaluates to.
- **When to Use**: When a branch or filter applies if **any** of several reified conditions are met:

```prolog
% INCORRECT (Impure soft-cut disjunction)
can_access_admin(Role, Access) :-
    ( (Role == admin ; Role == superuser) -> Access = granted ; Access = denied ).

% CORRECT (Pure reified disjunction via ';'/3)
can_access_admin(Role, Access) :-
    if_((=(Role, admin) ; =(Role, superuser)),
        Access = granted,
        Access = denied).

% Inside tfilter/3 to keep vowels:
is_vowel_t(Char, Truth) :-
    (=(Char, 'a') ; =(Char, 'e') ; =(Char, 'i') ; =(Char, 'o') ; =(Char, 'u'), Truth).

vowels_only(Chars, Vowels) :-
    tfilter(is_vowel_t, Chars, Vowels).
```

---

#### 4. Reified Conditional Execution: `cond_t/3` — When & How to Use
- **Mechanism**: `cond_t(If_1, Then_0, Truth)` executes `Then_0` when `If_1` holds, and simultaneously binds `Truth = true`. If `If_1` is false, it skips `Then_0` and binds `Truth = false`.
- **When to Use `cond_t/3`**: When you need to optionally execute a transformation/action **AND** return a boolean flag to the caller indicating whether the transformation occurred:

```prolog
% Attempt to apply a macro expansion rule, binding WasExpanded to true or false:
try_macro_expansion(Rule, TermIn, TermOut, WasExpanded) :-
    cond_t(subsumes_rule_t(Rule, TermIn),
           apply_rule(Rule, TermIn, TermOut),
           WasExpanded).
```

- **When to Use `cond_t/2`**: When you only want the conditional action executed and do not need to inspect the resulting truth value:
```prolog
audit_admin_action(User, IsAdmin) :-
    cond_t(IsAdmin, log_admin_audit(User)).
```

---

#### 5. Reified List Membership: `memberd_t/3`
Deterministic membership test without cuts; pure on open list tails:
```prolog
% INCORRECT (Impure memberchk)
check_permission(User, AllowedUsers, Status) :-
    ( member(User, AllowedUsers) -> Status = granted ; Status = denied ).

% CORRECT (Pure reified membership)
check_permission(User, AllowedUsers, Status) :-
    if_(memberd_t(User, AllowedUsers), Status = granted, Status = denied).
```

---

#### 6. Existential Searches: `tmember/2` & `tmember_t/3`
- **`tmember(Closure_2, List)`**: Finds list elements satisfying `call(Closure_2, X, true)`. Once an element deterministically satisfies the closure, no redundant choice point is left:
  ```prolog
  % Finds the first positive integer in List:
  find_positive(List, Pos) :-
      tmember(=(Pos), List),
      Pos #> 0.
  ```
- **`tmember_t(Closure_2, List, Truth)`**: Reifies the existential question (*"Does ANY element in List satisfy Closure_2?"*) into `true` or `false`:
  ```prolog
  % Reifies whether a list contains any active sessions:
  has_active_session(Sessions, HasActive) :-
      tmember_t(is_active_session_t, Sessions, HasActive).
  ```

---

#### 7. Pure Higher-Order List Filtering: `tfilter/3` & Partitioning: `tpartition/4`
```prolog
even_t(N, Truth) :-
    Rem #= N mod 2,
    =(Rem, 0, Truth).

% Filters even numbers purely in all directions:
filter_evens(Numbers, Evens) :-
    tfilter(even_t, Numbers, Evens).

% Direct Closure Passing: Filters all elements equal to 5
% (Passes =(5) directly as a closure, which internally invokes =(5, X, Truth) via (=)/3):
filter_fives(Numbers, Fives) :-
    tfilter(=(5), Numbers, Fives).

% Partitions numbers into Evens and Odds in a single pure pass:
separate_parity(Numbers, Evens, Odds) :-
    tpartition(even_t, Numbers, Evens, Odds).
```

### 7.4 Legitimate Circumstances for Legacy Built-ins
While declarative replacements should be used for all application and domain logic, legacy built-ins are legitimately used in specific low-level boundaries:

1. **Floating-Point Calculations**:
   - `is/2`, `float/1`, and standard arithmetic functions (`sin/1`, `cos/1`, `sqrt/1`) are legitimate when performing IEEE 754 floating-point calculations where pure real-number solvers (`clp(r)`) are unavailable.
2. **Standard Order of Terms (`compare/3`, `@<`, `@>`)**:
   - Deterministic key comparison on **known ground terms** when sorting keys or balancing pure binary search trees (`library(assoc)`).
3. **Foreign / Hardware I/O Boundaries (`var/1`, `nonvar/1`, `ground/1`)**:
   - Low-level driver code communicating with non-logical hardware packets, network sockets, or C/Rust FFI where argument serialization format must be checked before stream transmission.

---

## 8. Data Representation & Types

### 8.1 Clean vs. Defaulty Data Modeling
Distinguish distinct terms and AST variants using clear principal functors rather than defaulty fallthrough logic:

```prolog
% INCORRECT (Defaulty: numbers, variables, and terms mixed without explicit wrappers)
eval_node(N, N) :- number(N).
eval_node(plus(A, B), Res) :- eval_node(A, VA), eval_node(B, VB), Res #= VA + VB.

% CORRECT (Clean: distinguished by functor)
eval_node(num(N), N).
eval_node(add(A, B), Res) :-
    eval_node(A, VA),
    eval_node(B, VB),
    Res #= VA + VB.
```

### 8.2 Strings as Character Lists (`chars`)
- Treat strings **exclusively as lists of characters** (`chars`).
- Enforce `double_quotes` as `chars` in all modules (`:- set_prolog_flag(double_quotes, chars).`).
- **NEVER** use SWI-specific `string` types, atom-strings, or packed strings in portable logic.

```prolog
% CORRECT (Pure character list handling)
greet(Name, Greeting) :-
    phrase(("Hello, ", Name, "!"), Greeting).
```

### 8.3 Safe Type Testing (`library(si)`)
Use safe, non-raising type assertions from `library(si)` (`atom_si/1`, `list_si/1`, `integer_si/1`) rather than unsafe built-ins like `is_list/1` or raw type tests that raise instantiation errors on unbound variables.

### 8.4 ISO Standard Error Terms & Exception Hygiene (`error(Formal, Context)`)
When raising exceptions with `throw/1`, **always** conform to the ISO standard structured error format `error(Formal, Context)`.

1. **Standard ISO `Formal` Terms**:
   - `instantiation_error`: An argument was uninstantiated when a ground term was required.
   - `type_error(ValidType, Culprit)`: Culprit has an invalid type (e.g., `type_error(list, Culprit)`).
   - `domain_error(ValidDomain, Culprit)`: Culprit has the correct type but falls outside valid domain bounds (e.g., `domain_error(not_less_than_zero, -1)`).
   - `existence_error(ObjectType, Culprit)`: The referenced resource does not exist (e.g., `existence_error(source_sink, "config.json")`).
   - `permission_error(Operation, PermissionType, Culprit)`: An illegal operation was attempted (e.g., modifying a read-only stream).
   - `representation_error(Flag)`: An implementation limit was exceeded (e.g., `representation_error(character_code)`).
   - `evaluation_error(Error)`: Arithmetic or evaluation failure (e.g., `evaluation_error(zero_divisor)`).

2. **Exception Handling with `catch/3`**:
   ```prolog
   % INCORRECT (Impure: throwing bare atoms or strings)
   validate_age(Age) :-
       ( Age < 0 -> throw('age must be positive') ; true ).

   % CORRECT (Structured ISO error term with predicate context)
   %% validate_age(+Age) is det.
   validate_age(Age) :-
       (   integer_si(Age) ->
           (   Age #>= 0 -> true
           ;   throw(error(domain_error(not_less_than_zero, Age), validate_age/1))
           )
       ;   throw(error(type_error(integer, Age), validate_age/1))
       ).

   % Safe Exception Recovery:
   safe_read_config(File, Config) :-
       catch(load_config_file(File, Config),
             error(existence_error(source_sink, File), _Context),
             Config = default_config).
   ```

### 8.5 Attributed Variables (`library(atts)`) for Extensible Metadata
Attributed variables allow programs to attach arbitrary user-defined terms (domains, type bounds, AST provenance, constraint networks) directly to logical variables without modifying predicate signatures.

- **Mechanism**: Declared via `:- attribute Name/Arity.`. When an attributed variable is unified with another term or variable, the engine automatically invokes `verify_attributes/3` to enforce domain consistency or propagate constraints.
- **Foundation of Constraint Solvers**: Attributed variables form the foundational architecture of `library(clpz)`, `library(clpb)`, and domain-specific constraint engines:
  ```prolog
  :- use_module(library(atts)).
  :- attribute non_zero/0.

  % When unified, verify that the value is not zero:
  verify_attributes(Var, Other, Goals) :-
      (   get_atts(Var, non_zero) ->
          (   var(Other) ->
              put_atts(Other, non_zero),
              Goals = []
          ;   dif(Other, 0),
              Goals = []
          )
      ;   Goals = []
      ).
  ```

### 8.6 Standard `Key-Value` Pairs (`-`) & $O(N \log N)$ `keysort/2`
In ISO Prolog, key-value associations are canonically represented using the infix hyphen functor `-` as `Key-Value`.

1. **Standard Term Order Sorting (`keysort/2`)**:
   - `keysort/2` sorts a list of `Key-Value` pairs in **stable $O(N \log N)$ time** strictly by `Key` (using the standard order of terms `@<`).
   - **Preserves Duplicates**: Unlike `sort/2` which discards duplicate terms, `keysort/2` is **stable** and retains duplicate keys and their original relative ordering:
   ```prolog
   ?- keysort([3-c, 1-a, 2-b, 1-z], Sorted).
      Sorted = [1-a, 1-z, 2-b, 3-c].
   ```

2. **Pure Grouping by Key (`group_pairs_by_key/2`)**:
   - Combining `keysort/2` with a linear pass produces an optimal $O(N \log N)$ grouping algorithm:
   ```prolog
   %% group_pairs(+Pairs, -Grouped) is det.
   %  Sorts pairs by key and groups values sharing identical keys into lists.
   group_pairs(Pairs, Grouped) :-
       keysort(Pairs, Sorted),
       group_sorted_pairs(Sorted, Grouped).

   group_sorted_pairs([], []).
   group_sorted_pairs([K-V|Rest], [K-[V|Vs]|Grouped]) :-
       same_key_values(Rest, K, Vs, Unprocessed),
       group_sorted_pairs(Unprocessed, Grouped).

   same_key_values([K-V|Rest], K, [V|Vs], Unprocessed) :-
       !, % CUT JUSTIFICATION: Key identity check on ground sorted keys for deterministic partition
       same_key_values(Rest, K, Vs, Unprocessed).
   same_key_values(Unprocessed, _K, [], Unprocessed).
   ```

---

## 9. Definite Clause Grammars (DCGs) & Parsing

### 9.1 Pure DCGs as the Primary Default
Prefer pure Definite Clause Grammars (`library(dcgs)`) as the **standard default** for text matching, domain-specific grammars, lexing, formatting, and AST serialization.

- **When to Use DCGs**:
  - Context-free and declarative grammars (JSON, CSV, DSLs, configuration formats, math expressions).
  - Bidirectional serialization (generating character lists from ASTs via `phrase/2`).
  - Small-to-medium tokenizers and string matching relations.
  - **Implicit State Threading**: Monadic state propagation (e.g., symbol tables, accumulator counters, fresh variable name generation) across sequences of operations to prevent threading errors (`S0 -> S1 -> S2`).

- **When Alternative Parsing Architectures Are Justified**:
  - **Multi-Stage Compiler Pipelines**: Large language parsers (e.g. ISO Prolog syntax) often benefit from a dedicated lexer producing a `token(Kind, Value, Pos)` stream consumed by an AST parser over token lists.
  - **Source-Provenance & Position Tracking**: Compilers, debuggers, and IDE tools requiring granular byte offsets, line/column tracking, and rich source provenance may use explicit recursive descent state machines or position-threading clauses where DCG sugar adds friction.
  - **Operator-Precedence Parsers**: Dynamic operator precedences and binding powers (e.g., Pratt parsers for ISO `op/3` declarations) are often cleaner when implemented with explicit priority-driven loops.
  - **Streaming I/O**: High-throughput processing of large files via stream primitives (`get_char/2`, `read_line_to_chars/2`) to avoid buffering entire inputs into memory.

### 9.2 Purity & Prohibition of Cuts in DCGs
Cuts (`!`) in DCGs are **equally problematic—and often even more harmful**—than in regular Prolog code. Introducing cuts into DCGs breaks core declarative benefits:

1. **Destruction of Bidirectionality**: A pure DCG functions as both a parser (`phrase(grammar(AST), InputChars)`) and a serializer/generator (`phrase(grammar(AST), OutputChars)`). Cuts eliminate the ability to generate text or fuzz test valid grammatical terms from ASTs.
2. **Hidden Difference-List Scope Traps**: Because the DCG preprocessor automatically threads hidden difference-list arguments (`S0, S1, S`), cuts lock in difference-list unifications irreversibly, preventing backtracking across ambiguous prefix parses.
3. **Breakage of Grammar Combinators**: Higher-order DCG combinators (`phrase/3`, `seq//1`, `star//1`) rely on relational backtracking; embedded cuts escape local grammar scope and destroy combinator compositions.

| Aspect | Regular Prolog | Definite Clause Grammars (DCGs) |
| :--- | :--- | :--- |
| **Bidirectionality** | Lost on relations | Lost for parsing, serialization, and test generation |
| **Lookahead Alternative** | `if_/3`, `dif/2`, indexing | Pure pushback / semicontext (`[Lookahead] --> [Lookahead]`) |
| **Underlying Impact** | Prunes explicit choicepoints | Prunes hidden difference-list threading state |
| **Compositionality** | Breaks relational call chains | Breaks higher-order grammar combinators (`seq//1`, `star//1`) |

**Verdict**: Cuts in DCGs must be avoided with the same strict discipline as in general Prolog code. Lookahead and branch selection in DCGs should be handled via **first-token argument indexing**, **pushback semicontext lists**, and pure **reification (`if_`, `cond_t`)**.

### 9.3 Pure Lookahead & Pushback (No Cuts in DCGs)
Use pure DCG pushback / semicontext lists (`... , [Lookahead], ...`) instead of cuts (`!`) to inspect lookahead tokens without consuming them:

```prolog
% INCORRECT (Impure lookahead using cut)
keyword_or_ident(kw(if)) --> "if", !.
keyword_or_ident(id(Name)) --> ident(Name).

% CORRECT (Pure lookahead via pushback semicontext)
peek_char(Char), [Char] --> [Char].
```

### 9.4 State Threading in DCGs
When state threading is required across sequential steps, use DCGs as an implicit state monad as detailed in [Section 10.2](#102-dcg-difference-lists-as-implicit-state-monads).

---

## 10. State Management & Threading Architectures

### 10.1 The State Threading Challenge in Pure Logic
In pure logic programming, variables are single-assignment and there is no global mutable state. Complex compilers, interpreters, and domain applications must thread state across many operations. Without careful architectural design, naive state passing introduces two severe anti-patterns:
1. **Argument Explosion**: Predicates ballooning to 8–14 arguments passing multiple before/after pairs (`(Name0, NameOut, Exp0, ExpOut, Ops0, OpsOut, Stmts0, StmtsOut, State0, StateOut, OpTable0, OpTableOut)`).
2. **Threading Index Typos**: Manual index chains (`S0 -> S1 -> S2 -> S2 -> S4`) where an accidental typo quietly drops state updates or causes subtle variable aliasing bugs.

### 10.2 DCG Difference Lists as Implicit State Monads & Output Accumulators
DCGs provide built-in difference-list abstraction that can be leveraged for state propagation and output collection:

- **Implicit Single State Threading**: Use DCG semicontext accessors to read and update a threaded state term without manual variable indices:
  ```prolog
  % State accessors:
  state(S), [S] --> [S].
  state(S0, S), [S] --> [S0].

  % State-threaded sequence:
  eval_and_update(Expr) -->
      state(S0),
      compute_step(Expr, S0, S1),
      state(S0, S1).
  ```
- **Output Stream Accumulation**: When collecting lineages, AST nodes, or macro records, use DCG emission (`[Record]`) instead of threading manual accumulator lists and calling expensive `append/3`:
  ```prolog
  expand_term(Term, Expanded) -->
      [macro(dcg, Term)],
      { prolog_dcg_expand_rule(Term, Expanded) }.
  ```

### 10.3 Structured State / Builder Compound Terms (Preventing Argument Explosion)
When an operation requires threading multiple interrelated state channels, **pack related arguments into a single structured compound term** (Builder / State record) rather than passing separate parameter pairs:

```prolog
% ANTI-PATTERN: Argument explosion across 6 separate variable pairs (12 arguments)
update_module(Name0, Name, Exp0, Exp, Ops0, Ops, Stmts0, Stmts, State0, State, Table0, Table) :- ...

% CORRECT: Consolidated Builder Compound Term (2 arguments)
update_module(Builder0, BuilderOut) :-
    Builder0 = builder(Name, Exp, Ops0, Stmts, State0, Table0),
    add_operator(Table0, P, S, O, Table1),
    BuilderOut = builder(Name, Exp, [op(P,S,O)|Ops0], Stmts, State0, Table1).
```

### 10.4 Higher-Order State Folding (`foldl/N`)
When threading state through a sequence of items in a list, prefer `foldl/4` or `foldl/5` from `library(lists)` (or `library(lambda)`) over writing custom recursive loop predicates:

```prolog
% INCORRECT (Boilerplate recursive loop with manual state threading)
apply_all([], State, State).
apply_all([X|Xs], State0, StateOut) :-
    apply_one(X, State0, State1),
    apply_all(Xs, State1, StateOut).

% CORRECT (Declarative foldl)
apply_all(Items, State0, StateOut) :-
    foldl(apply_one, Items, State0, StateOut).
```

### 10.5 Macro & Term Expansion (`term_expansion/2`, `goal_expansion/2`)
When multiple clauses or rules share identical structural logic that differs only by data constants (such as character escape tables, opcode decoders, keyword lexers, or AST visitors), **do NOT duplicate boilerplate clauses manually**. Use compile-time macro expansion or data-driven relation tables to enforce DRY.

#### The Golden Rule: Prefer Batch Collection Macros (`maplist/3`) over Sequential Single-Item Invocations
When defining macro-expanded tables across a collection of elements, **always prefer a single batch collection macro (`maplist(Expand, Collection, Clauses)`) over repeated single-item top-level invocations (`f(x1). f(x2). f(x3). ...`)**.

```prolog
% ❌ ANTI-PATTERN: Repeated single-item macro invocations (Violates DRY)
char_to_esc('a').
char_to_esc('b').
char_to_esc('r').
char_to_esc('n').
char_to_esc('t').

% ❌ ANTI-PATTERN: Repeated keyword grammar rules (Violates DRY)
keyword(if)    --> "if".
keyword(then)  --> "then".
keyword(else)  --> "else".
keyword(while) --> "while".
```

#### Multi-Domain Batch Collection Macro Patterns (Option C)

##### Pattern 1: Character Escape Sequence Tables (`chars_to_escapes/1`)
```prolog
% Compile-time collection expansion:
user:term_expansion(chars_to_escapes(Chars), Clauses) :-
    maplist(make_escape_clause, Chars, Clauses).

make_escape_clause(Esc, (char_to_esc(C, Esc) :- true)) :-
    read_from_chars(['"', '\\', Esc, '"', '.'], [C]).

% Author declares the entire escape table in 1 line:
chars_to_escapes("abrntvf'\"\\").

% The parser rule remains completely clean and unified:
escape_sequence(Char) -->
    [EscChar],
    { char_to_esc(Char, EscChar) }.
```

##### Pattern 2: Programming Language Keywords & Token Tables (`keywords/1`)
```prolog
% Batch-generate grammar rules for an entire language keyword set:
user:term_expansion(keywords(KwList), Clauses) :-
    maplist(make_keyword_clause, KwList, Clauses).

make_keyword_clause(Kw, (keyword(Kw) --> Chars)) :-
    atom_chars(Kw, Chars).

% Author declares all language keywords in 1 clean collection:
keywords([if, then, else, elif, while, for, in, return, fn, let, match]).

% Clean DCG token parsing:
keyword_token(Token) -->
    keyword(Token).
```

##### Pattern 3: Bytecode Opcode & Instruction Decoders (`opcodes/1`)
```prolog
% Batch-generate instruction decoding relations from Key-Value pairs:
user:term_expansion(opcodes(Pairs), Clauses) :-
    maplist(make_opcode_clause, Pairs, Clauses).

make_opcode_clause(Byte-Name, (opcode_inst(Byte, Name) :- true)).

% Author declares entire instruction table compactly:
opcodes([
    0x01-iadd, 0x02-isub, 0x03-imul, 0x04-idiv,
    0x10-load, 0x11-store, 0x20-jump, 0x21-jz,
    0xFF-halt
]).
```

- **When to Use Batch Term Expansion**:
  - Expanding compact closed alphabets, keyword vocabularies, or opcode lists into indexed static lookup tables.
  - Automatically synthesizing clause families from declarative schema facts or grammar tables.
  - Compiling Domain Specific Languages (DSLs) into pure Prolog difference lists.
  - Generating Extended DCG (EDCG) state-threading code for multiple hidden accumulators.



### 10.6 Pure Associative Dictionaries (`library(assoc)`)
For dynamic symbol tables, variable environments, and key-value lookups:
- Use pure balanced binary tree maps from `library(assoc)` (`empty_assoc/1`, `get_assoc/3`, `put_assoc/4`).
- **NEVER** use imperative database mutations (`assertz/1`, `retract/1`, `bb_put/2`) as a substitute for threaded state.

```prolog
% CORRECT (Pure environment lookup and functional update)
bind_var(Var, Val, Env0, EnvOut) :-
    put_assoc(Var, Env0, Val, EnvOut).
```

### 10.7 Dynamic Predicates (`assertz`/`retract`) vs. Pure State: Architectural Boundaries

A common question in Prolog architecture is: *When should `assertz/1` and dynamic predicates be avoided, and when are they legitimate?*

#### 1. Why `assertz`/`retract` is Prohibited for Local Algorithm State
Using `assertz/1` and `retract/1` as mutable variables within algorithms, search routines, or parsing passes introduces serious architectural defects:

| Problem Domain | Pure Threaded State (`library(assoc)`, DCGs, Builders) | Dynamic Database Mutation (`assertz` / `retract`) |
| :--- | :--- | :--- |
| **Backtracking Safety** | **Sound**: State automatically unwinds and resets upon failure or backtracking. | **Unsound**: Asserted facts persist globally after failure, corrupting subsequent search paths. |
| **Re-entrancy & Threading** | **100% Re-entrant**: Concurrent threads or nested queries cannot interfere. | **Race Conditions**: Global mutable database collisions and lock contention. |
| **Performance & Memory** | **Fast $O(\log N)$**: Cleanly garbage-collected on the execution stack. | **High Overhead**: Dynamic index updates, clause reallocation, and database locks. |
| **Determinism & Reasoning** | **Referentially Transparent**: Relations are mathematical functions of their inputs. | **Hidden Dependencies**: Behavior depends invisibly on mutable global database history. |

#### 2. Static Compilation vs. Dynamic `assert` in Macro Expansion
- **Macro Expansion (`term_expansion/2`, `goal_expansion/2`) does NOT use `assert`**:
  - When the Prolog reader encounters term expansion hooks during file loading, the generated terms are handed directly to the **static clause compiler**.
  - The engine compiles these clauses into **immutable, heavily optimized static bytecode** (with hash-indexed jump tables and zero dynamic locking overhead).
  - Writing compile-time term expansions is completely pure and static—it has nothing to do with dynamic `assertz/1`.

#### 3. Legitimate Architectural Uses for `assertz` / Dynamic Database
`assertz/1`, `retract/1`, and `retractall/1` are legitimate and appropriate in specific, well-defined boundaries:

1. **Dynamic Plugin & Tool Registration**:
   - Registering user-installed skills, tool capability bundles, or dynamic foreign handlers at application startup (e.g., `agent_register_skill/2`).
2. **Interactive Deductive Knowledge Bases & Rule Learning**:
   - Interactive knowledge-base systems where users or autonomous agents discover, verify, and store new ground facts, ontology axioms, or persistent domain rules across sessions.
3. **Global Persistent Configuration**:
   - Truly global application environment settings or resource descriptors that must outlive individual query lifecycles.
4. **Implementing Tabling / Memoization Engines**:
   - Internal engine-level SLG trie tables (though application programmers should use `:- table` declarations directly rather than writing manual `assert`-based memoization).

#### 4. Summary Decision Matrix

```
Is the state needed only within a single query, transaction, or compiler pass?
  ├── YES → Use pure threaded state (library(assoc), DCG state monad, or foldl/N).
  └── NO  ── Are you generating boilerplate clauses at compile time?
               ├── YES → Use term_expansion/2 (compiles to static code, not dynamic assert).
               └── NO  ── Is it a persistent knowledge base or dynamic plugin registry?
                            └── YES → Use assertz/1 with explicit :- dynamic declarations.
```

---

## 11. Text Formatting, I/O & Separation of Concerns

### 11.1 Separation of Pure Computation from I/O
- Keep computational logic, data transformation, and text serialization 100% pure.
- Confine stream I/O (`read_line_to_chars`, `write`, `format`) to top-level command boundaries.

### 11.2 Unified Format Calls (One Call vs. Chained Calls)
When using formatting predicates (`format/2`, `format/3`, `format_chars/2`, or DCG formatting rules):
- **Rule**: Prefer a **single format call on a unified/joined format string** over multiple sequential format calls.
- **Rationale**: Reduces I/O calls, minimizes context switches, avoids fragmented buffers, and enhances code readability.

```prolog
% INCORRECT (Multiple fragmented format calls)
print_report(User, Score, Rank) :-
    format("User: ~s", [User]),
    format(" | Score: ~d", [Score]),
    format(" | Rank: ~d~n", [Rank]).

% CORRECT (One unified format call with complete argument vector)
print_report(User, Score, Rank) :-
    format("User: ~s | Score: ~d | Rank: ~d~n", [User, Score, Rank]).
```

### 11.3 Pure String Construction via `charsio` & DCGs
Prefer constructing character lists using DCGs and `phrase/2` or `library(charsio)` (`format_to_chars/3`) before writing to streams, keeping rendering logic separate from side-effecting I/O.

---

## 12. Declarative Constraint Systems (`CLP(Z)`, `CLP(B)`, `CLP(FD)`)

### 12.1 The Declarative Constraint Advantage (Constrain-and-Generate)
Traditional imperative programming and early Prolog code relied on **generate-and-test** (generating possible candidates first, then testing guards), which causes catastrophic combinatorial explosion.

Modern Prolog takes full advantage of **declarative constraint systems** (**constrain-and-generate**):
- **Early Pruning**: Constraints posted on variables prune impossible domain values *immediately*, before any search choices are made.
- **True Mathematical Relations**: Equations work bidirectionally without manual rearrangement or mode declarations.
- **Delayed Evaluation**: Constraints remain active across uninstantiated variables, suspending until sufficient information arrives.

### 12.2 Integer Constraints (`library(clpz)` / `library(clpfd)`)
- **When to Use**: All integer arithmetic, sequence lengths, array/list indices, resource counting, discrete optimization, scheduling, and mathematical relationships ($\mathbb{Z}$).
- **Core Relations**: `#=`, `#\=`, `#>`, `#<`, `#>=`, `#=<`, `in`.
- **Global Constraints**: `all_different/1` (or `all_distinct/1`) to enforce pairwise distinctness with maximum propagation efficiency.

```prolog
% CORRECT (Bidirectional integer sum relation)
sum_list([], 0).
sum_list([X|Xs], Sum) :-
    Sum #= X + Rest,
    sum_list(Xs, Rest).

% Cryptarithmetic / Permutation constraint modeling:
send_more_money([S,E,N,D,M,O,R,Y]) :-
    Vars = [S,E,N,D,M,O,R,Y],
    Vars ins 0..9,
    all_different(Vars),
    S #\= 0, M #\= 0,
                 1000*S + 100*E + 10*N + D
    +            1000*M + 100*O + 10*R + E
    #= 10000*M + 1000*O + 100*N + 10*E + Y.
```

### 12.3 Boolean Constraints (`library(clpb)`)
- **When to Use**: Propositional logic reasoning, SAT solving, digital circuit simulation/verification, theorem proving, and cardinality constraints over sets of feature flags or security policies.
- **Core Relations**:
  - `sat(Formula)`: Posts a boolean equation that must hold over $\{0, 1\}$.
  - `taut(Formula, Truth)`: Proves whether a formula is a universal tautology (`Truth = 1`) or not (`Truth = 0`).
  - **Operators**: `*` (AND), `+` (OR), `#` (XOR), `-` (NOT), `=:=` (equivalence), `=\=` (non-equivalence), `=<` (implication), `card(Counts, Vars)` (cardinality).

```prolog
% 1. Universal Theorem Proving: Verify De Morgan's Law
verify_demorgan(IsTautology) :-
    taut(-(A * B) =:= -A + -B, IsTautology). % Yields IsTautology = 1

% 2. Cardinality Constraints over Feature Flags (e.g. Exactly 1 active plan):
valid_subscription(Free, Pro, Enterprise) :-
    sat(card([1], [Free, Pro, Enterprise])).

% 3. Digital Logic Circuit: Half-Adder
half_adder(A, B, Sum, Carry) :-
    sat(Sum =:= A # B),
    sat(Carry =:= A * B).
```

### 12.4 Constraint System Selection Guide (`CLP(Z)` vs. `CLP(B)` vs. `library(reif)`)

To choose the appropriate declarative tool, consult the following decision matrix:

| Task / Domain | Recommended Tool | Key Primitives | Why & When to Choose |
| :--- | :--- | :--- | :--- |
| **Control Flow & Term Discrimination** | `library(reif)` | `if_/3`, `=(X,Y,T)`, `dif/2`, `memberd_t/3`, `tfilter/3` | Operates on **arbitrary Prolog terms** (`atoms`, `lists`, `chars`, `ASTs`, structures). Pure replacement for `-> / ;` and `memberchk/2`. |
| **Integer Arithmetic & Intervals** | `library(clpz)` / `clpfd` | `#=`, `#\=`, `#>`, `in`, `zcompare/3`, `all_different/1` | Reasoning over **integers ($\mathbb{Z}$)**, ranges, discrete counting, scheduling, and arithmetic equations. |
| **Propositional Logic, SAT & Circuit Rules** | `library(clpb)` | `sat/1`, `taut/2`, `card/2`, `*`, `+`, `#` | Global BDD-based reasoning over **Boolean formulas and $\{0, 1\}$ variables**. Ideal for SAT, tautology proofs, and cardinality flags. |

### 12.5 Separation of Modeling from Search (Labeling Strategies)
In constraint programming, **strictly separate constraint posting (modeling) from concrete value enumeration (search)**:

1. **Phase 1 (Modeling)**: Post all domain bounds and arithmetic/boolean constraints. This deterministically narrows domains without creating choice points.
2. **Phase 2 (Search)**: Invoke `label/1` or `labeling/2` **only at the query boundary or solution generator**, never interleaved inside internal relational clauses:

```prolog
% INCORRECT (Premature enumeration inside relational predicate)
bad_range(X) :-
    X in 1..100,
    label([X]), % Premature choicepoint!
    X #> 50.

% CORRECT (Post all constraints first, label at boundary)
solve_puzzle(Vars) :-
    post_puzzle_constraints(Vars),
    labeling([ff, bisect], Vars).
```

### 12.6 Reified Arithmetic Comparison (`zcompare/3`)
Use `zcompare(Order, X, Y)` for pure ternary comparison (`<`, `=`, `>`) of integer expressions in conditionals, avoiding cuts or non-logical comparison ladders:

```prolog
classify_integer(N, Class) :-
    zcompare(Order, N, 0),
    if_(Order = (<), Class = negative,
        if_(Order = (=), Class = zero, Class = positive)).
```

---

## 13. Module Architecture, Exports & Meta-Predicates

### 13.1 Module Headers & Explicit Imports
- Explicitly declare module headers `:- module(Name, [Exports...]).`.
- Explicitly declare all library dependencies (`:- use_module(library(dcgs)).`, `:- use_module(library(reif)).`). Do not rely on implicit autoloading.

### 13.2 Meta-Predicate Declarations (`meta_predicate`)
For higher-order predicates accepting goals or closures, always provide explicit `:- meta_predicate` declarations directly under the module header:

```prolog
:- module(list_utils, [filter_list/3]).
:- meta_predicate filter_list(2, +, -).
```

### 13.3 Homoiconicity & Term Representations
Represent agent capabilities, skills, and configuration facts as pure Prolog terms:
```prolog
skill(prolog_conventions, [purity, dcg, clp, type_testing, strings]).
```

### 13.4 Tabling / Memoization (SLG Resolution) for Cyclic Graphs & Transitive Closures
Standard Prolog execution (SLD resolution) suffers from non-termination on left-recursive rules and cyclic graphs. **Tabling** (SLG resolution) memoizes subgoals and their answer sets, guaranteeing termination for Datalog programs and cyclic structures without manual visited-node sets.

- **Declaration**: `:- table PredicateIndicator, ...`.
- **Cyclic Graph Reachability**:
  ```prolog
  :- use_module(library(tabling)).
  :- table path/2.

  % Graph with cyclic edges (1 -> 2 -> 1):
  edge(1, 2).
  edge(2, 1).
  edge(2, 3).

  % Pure transitive closure with tabling terminates cleanly:
  path(X, Y) :- edge(X, Y).
  path(X, Y) :- path(X, Z), edge(Z, Y).
  ```

### 13.5 Homoiconic Meta-Interpreter Scaffolding (The `mi/1` Pattern)
Because Prolog is **homoiconic** (Prolog programs are themselves first-class Prolog data terms), building custom interpreters, execution tracers, proof-tree generators, and bounded evaluators requires only minimal meta-interpreter scaffolding:

1. **The Classic 3-Clause Vanilla Meta-Interpreter**:
   ```prolog
   %% mi(+Goal) is nondet.
   %  Executes pure Prolog Goal via meta-interpretation.
   mi(true).
   mi((A, B)) :-
       mi(A),
       mi(B).
   mi(Goal) :-
       dif(Goal, true),
       dif(Goal, (_, _)),
       clause(Goal, Body),
       mi(Body).
   ```

2. **Step-Counting / Resource-Bounded Meta-Interpreter**:
   - Easily extended to track inference depth or enforce computational budgets:
   ```prolog
   %% mi_bounded(+Goal, +MaxSteps, -RemainingSteps) is semidet.
   mi_bounded(true, Steps, Steps).
   mi_bounded((A, B), Steps0, Steps) :-
       mi_bounded(A, Steps0, Steps1),
       mi_bounded(B, Steps1, Steps).
   mi_bounded(Goal, Steps0, Steps) :-
       Steps0 #> 0,
       Steps1 #= Steps0 - 1,
       dif(Goal, true),
       dif(Goal, (_, _)),
       clause(Goal, Body),
       mi_bounded(Body, Steps1, Steps).
   ```

---

## 14. Execution Safety, Timeouts & Sandboxing

### 14.1 21-Second Default Timeout
- All query executions, top-level queries (`prolog-agent query`), interactive REPL sessions (`prolog-agent repl`), and test runners enforce a **21.0-second default safety timeout** (unless overridden via `--timeout` or `PROLOG_TIMEOUT`).

### 14.2 Fibonacci Continuation Progression (34s, 55s, 89s...)
- In interactive sessions, if a query hits the 21s timeout, the process tree is suspended (`SIGSTOP`), freezing CPU to 0% while preserving memory state.
- The user is prompted to extend execution by the next Fibonacci increment (**34s**, then **55s**, **89s**, **144s**...) via `SIGCONT`, or terminate the query cleanly.
- Non-interactive (CI/CD, scripts) environments terminate immediately upon initial timeout expiration.

### 14.3 Mandatory Safety Wrappers
- **MANDATORY**: Run all Prolog code via safety wrappers (`prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`).
- **FORBIDDEN**: Never invoke raw interpreter binaries (`scryer-prolog`, `swipl`, `tpl`) directly without safety wrappers.

---

## 15. Anti-Patterns & Prohibited Constructs

| Prohibited Anti-Pattern | Required Pure Pattern | Rationale |
| :--- | :--- | :--- |
| `A is B + 1` for integers | `A #= B + 1` (`library(clpz)`) | Bidirectional relations; handles uninstantiated variables without crashing |
| `( Cond -> Then ; Else )` | `if_(Cond_t, Then, Else)` (`library(reif)`) | Preserves alternate branches when condition is uninstantiated |
| `\+ X = Y` or `X \= Y` | `dif(X, Y)` | Sound term inequality without premature failure |
| `if_(X = Y, T = true, T = false)` | `=(X, Y, T)` | Direct reification (DRY) |
| `memberchk(X, List)` | `memberd_t(X, List, true)` | Pure deterministic membership without cuts |
| `include(Goal, List, Out)` | `tfilter(Closure_t, List, Out)` | Pure higher-order list filtering |
| Chained `format("~s", [A]), format("~d", [B])` | `format("~s~d", [A, B])` | Single unified format call |
| Cuts (`!`) for flow control | `if_/3`, `cond_t`, indexing | Preserves multidirectional search |
| SWI `string` types / dicts in portable code | ISO `chars` lists / clean terms | Portability across all ISO-compliant engines |
| Raw binary execution (`scryer-prolog`) | `scryer-safe` / `prolog-safe` | Memory, CPU quota, and 21s timeout sandboxing |
| Missing goal-per-line formatting | 1 goal per line, 4-space indent | Clear visual logical structure (Covington) |
| Missing doc headers on public predicates | `%% Name(+Arg, -Res) is Det.` | Structured contract for humans and AI agents |
| Argument explosion (8+ parameters) | Builder compound term `builder(...)` | Eliminates argument clutter and threading typos |
| Imperative state mutation (`assertz`/`retract`) | Pure `library(assoc)` / threaded state | Avoids side-effecting global state corruption |
| Bare atom exceptions (`throw(bad_input)`) | ISO structured term `throw(error(Formal, Context))` | Interoperable, catchable ISO error hygiene |
| Body recursion on large lists (`O(N)` stack) | Tail recursion with accumulator + TCO | Prevents stack overflows; executes in $O(1)$ stack space |
| Dispatch discriminator in 2nd/3rd argument | First-argument functor indexing | Engine jumps in $O(1)$ without allocating choice points |
| Unsound sorting / loss of duplicate keys | Stable `keysort/2` over `Key-Value` pairs | Preserves key-value stability in $O(N \log N)$ time |
| Manual cyclic path detection loops | Tabling / SLG resolution (`:- table path/2.`) | Sound termination over cyclic graphs and Datalog relations |


