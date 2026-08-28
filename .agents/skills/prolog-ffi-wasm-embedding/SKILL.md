---
name: prolog-ffi-wasm-embedding
description: Guidelines for embedding Prolog engines and interfacing via Foreign Function Interfaces (FFI) and WebAssembly (WASM). Use when connecting Prolog logic to C, Rust, Python, JavaScript, and Node.js.
---

# Prolog FFI & WASM Embedding Guidelines

Use this skill when integrating Prolog knowledge bases or solver engines into hybrid applications written in Python, Rust, C, JavaScript, or WebAssembly.

## 1. Engine & FFI Capabilities Matrix

| Engine | Primary FFI / Interfacing Language | WASM Support | Common Use Cases |
| :--- | :--- | :--- | :--- |
| **SWI-Prolog** | Python (`janus-swi`), C/C++ FFI | SWI WASM | Enterprise Python/Prolog AI pipelines, web apps |
| **Scryer Prolog** | Rust (`scryer-prolog` crate) | WASM Target | High-performance pure Prolog in Rust binaries & WASM |
| **Trealla Prolog** | C FFI, WASM (`tpl.wasm`) | First-class WASM | Fast edge compute, microservices, containerized WASM |
| **Tau Prolog** | JavaScript / Node.js native | Native JS | Web browser DOM manipulation & client-side logic |

---

## 2. Python Integration (`janus-swi`)

In SWI-Prolog environment, use Janus to call Python from Prolog and vice versa:

```python
# Calling Prolog from Python
from janus_swi import Query

with Query("n_queens(8, Qs)") as q:
    while q.nextSolution():
        print(q.val("Qs"))
```

```prolog
% Calling Python from Prolog
:- use_module(library(janus)).

call_py_math :-
    py_call(math:sin(0.5), Result),
    writeln(Result).
```

---

## 3. Browser & JavaScript Integration (Tau Prolog / Trealla WASM)

### Tau Prolog (Browser DOM)
```javascript
const session = pl.create(1000);
session.consult(`
    :- use_module(library(dom)).
    greet(Name) :-
        get_by_id("output", Elem),
        set_html(Elem, Name).
`);
session.query("greet('Hello World').");
session.answer();
```

---

## 4. Safety Considerations

- Always sanitize inputs passed across language boundaries to prevent code injection into `consult/1` or `read_term/2`.
- Enforce CPU and memory limits on foreign calls using process isolation or `prolog-safe` sub-processes.
