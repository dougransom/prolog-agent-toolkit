# Prolog Agent Toolkit Glossary & Terminology Index

This glossary provides authoritative definitions for key Prolog concepts, dialect rules, purity guidelines, and safety constructs used throughout `prolog-agent-toolkit`.

---

## 1. Core Prolog & Logic Concepts

### Logical Purity
The design principle of writing Prolog goals such that they retain sound logical semantics regardless of mode (input/output instantiation). Pure Prolog avoids non-logical cuts (`!`), side-effects during search, and negation-as-failure (`\+/1`) where pure reification (`if_/3`, `dif/2`) can be used.

### `if_/3` & Reification ([`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl))
A pure boolean condition evaluator that reifies a truth value (`true` or `false`) to avoid choice-points and cuts.
- **Example**: `if_(X = Y, ActionA, ActionB)`
- **Rule**: Prefer isolating the test-value relation: `if_(G, A="A", A="B"), write(A)`.

### `dif/2`
A pure sound inequality constraint stating that two terms `X` and `Y` are not unifiable. Unlike `\+ (X = Y)`, `dif(X, Y)` suspends until terms are sufficiently instantiated, guaranteeing logical soundness.

### Chars Strings
In [Scryer Prolog](https://github.com/mthom/scryer-prolog) and standard [ISO Prolog](https://www.iso.org/standard/21413.html), double-quoted strings `"hello"` represent lists of single-character atoms: `['h', 'e', 'l', 'l', 'o']`. Raw string primitives (such as [SWI-Prolog](https://www.swi-prolog.org/) string types) are prohibited in ISO-pure code.

### Definite Clause Grammars (DCG)
Pure rule-based parsing and generation syntax using `-->`. DCGs build ASTs, parse tokens, and serialize data cleanly without imperative loops or side-effects.

---

## 2. Dialect & Engine Terminology

### [Scryer Prolog](https://github.com/mthom/scryer-prolog)
An ISO-compliant Prolog engine written in Rust emphasizing purity, module safety, [`CLP(Z)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl), pure DCGs, and `chars` string representations.

### [SWI-Prolog](https://www.swi-prolog.org/)
A widely used Prolog environment providing module extensions, SWI dicts, string types, and `plunit` testing framework.

### [Trealla Prolog](https://github.com/trealla-prolog/trealla)
A lightweight ISO-compliant C-based Prolog interpreter targeted at fast startup, WASM embedding, and standard library parsing.

### [Tau Prolog](http://tau-prolog.org/)
An ISO-compliant Prolog interpreter written in JavaScript for running directly inside web browsers and Node.js DOM environments.

---

## 3. Toolkit Execution Safety & Packaging

### Safety Runner (`prolog-safe`, `scryer-safe`, `swi-safe`)
Cross-platform execution wrappers provided by `prolog_agent_toolkit/runner.py` that execute Prolog goals under CPU time limits and memory quotas, preventing runaway infinite loops or OS crashes.

### Bakage (`bakage.toml`)
The package manifest format used by Scryer Prolog to declare project metadata, exported modules, and dependencies.

### Covington Style Guide
A classic style guide for Prolog programming ([.agents/references/covington_style.md](../.agents/references/covington_style.md)) emphasizing readability, explicit goal ordering, simple clause structures, and human-first layout.

---

## 4. System Architecture & Metadata

### Repository Ontology
The machine-readable component graph ([`docs/repository_ontology.json`](repository_ontology.json)) and human-readable architecture overview ([`docs/ONTOLOGY.md`](ONTOLOGY.md)) mapping all modules, CLI entry points, subagents, and directed file dependencies.
- **Human-Readable Guide**: [`docs/ONTOLOGY.md`](ONTOLOGY.md)
- **Machine-Readable Graph**: [`docs/repository_ontology.json`](repository_ontology.json)
- **Capability Registry**: [`docs/capability_manifest.json`](capability_manifest.json)

