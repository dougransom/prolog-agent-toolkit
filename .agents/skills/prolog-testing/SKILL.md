---
name: prolog-testing
description: Standardized instructions and frameworks for writing and running Prolog unit tests across engines (Scryer testing.pl, SWI plunit, Trealla/ISO).
---

# Prolog Testing Standards

Use this skill when writing, running, or configuring unit tests for Prolog code.

## Scryer Prolog (Primary / Default Engine)

For Scryer Prolog, use [`testing.pl`](https://github.com/bakaq/testing.pl).

### Installing / Referencing `testing.pl`
Fetch `testing.pl` into the project's test directory or library path:
```prolog
:- use_module(library(testing)).
```
Or reference a local `testing.pl` module:
```prolog
:- use_module('tests/testing.pl').
```

### Writing Tests in Scryer Prolog
Use `test/1` or `test/2` predicates:
```prolog
:- use_module(library(testing)).

test(pure_addition) :-
    X = 3,
    Y = 4,
    Z is X + Y,
    Z == 7.

test(dcg_parse) :-
    phrase("hello", `hello`).
```

### Running Scryer Prolog Tests Safely
Always run tests using `scryer-safe`:
```bash
scryer-safe -g run_tests -t halt tests/test_suite.pl
```

---

## SWI-Prolog Testing

For SWI-Prolog, use `library(plunit)`.

```prolog
:- use_module(library(plunit)).

:- begin_tests(basic_tests).

test(addition) :-
    X is 2 + 2,
    X == 4.

:- end_tests(basic_tests).
```

### Running SWI-Prolog Tests Safely
```bash
swi-safe -g "run_tests,halt" tests/test_suite.pl
```

---

## Trealla / Portable ISO Testing

For Trealla or generic ISO engines, write pure assertion runner predicates evaluated via `trealla-safe` or `prolog-safe`.
```prolog
run_all_tests :-
    (   test_clause1, test_clause2 ->
        write('ALL TESTS PASSED'), nl
    ;   write('TEST FAILURE'), nl, halt(1)
    ).
```
```bash
trealla-safe -g "run_all_tests,halt" tests/test_suite.pl
```
