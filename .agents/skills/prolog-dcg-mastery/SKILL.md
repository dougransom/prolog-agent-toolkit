---
name: prolog-dcg-mastery
description: Definite Clause Grammar (DCG) standards and advanced patterns. Use when parsing text, lexing tokens, building ASTs, generating binary/text output, handling lookahead without cuts, error recovery, and using pushback lists.
---

# Definite Clause Grammar (DCG) Mastery Guidelines

Use this skill when designing grammars, tokenizers, parsers, abstract syntax tree (AST) generators, or sequence serializers in Prolog.

## 1. Core Syntax & Modules

Always include standard DCG libraries across engines:

- **Scryer Prolog**: Requires explicit module import:
  ```prolog
  :- use_module(library(dcgs)).
  :- use_module(library(charsio)).
  ```
- **SWI / Trealla / Tau**: Standard syntax built-in or provided via standard library.

### ISO DCG Export & Import Notation (`Name//Arity`)

When defining modules or importing DCG non-terminals, always use the ISO double-slash convention (`Name//Arity` where `Arity` is the number of explicit DCG rule arguments):

```prolog
% Exporting a DCG non-terminal in a module header:
:- module(json_parser, [
    json_value//1,   % DCG non-terminal with 1 argument (expands to json_value/3)
    json_object//1
]).

% Importing specific DCG non-terminals from another module:
:- use_module(json_parser, [
    json_value//1
]).
```

---

## 2. Bidirectional Parsing & Serialization

Structure DCG rules so they operate bi-directionally whenever possible:

```prolog
% Rule parses a sequence of digits to an integer or formats an integer to chars
integer_ast(N) -->
    digits(Ds),
    { Ds \= [], number_chars(N, Ds) }.

digits([D|Ds]) --> digit(D), digits(Ds).
digits([])     --> [].

digit(D) --> [D], { member(D, "0123456789") }.
```

---

## 3. Pure Lookahead & Pushback Lists

Avoid non-logical cuts (`!`) inside DCG rules. Use **Pushback Lists** (right-hand side context insertion `[X], ...`) to implement lookahead cleanly:

```prolog
% Lookahead: inspect next character C without consuming it
peek(C), [C] --> [C].

% Rule matching an identifier until a delimiter without consuming the delimiter
identifier([C|Cs]) -->
    [C],
    { char_type(C, alphanumeric) },
    !, % Local deterministic match
    identifier(Cs).
identifier([]) --> [].
```

---

## 4. AST Construction Patterns

Pass AST accumulator variables in rule arguments:

```prolog
expr(bin_op(Op, Left, Right)) -->
    term(Left),
    op(Op),
    expr(Right).
expr(Term) --> term(Term).

op(+) --> "+".
op(-) --> "-".
op(*) --> "*".
```

---

## 5. Token Streams & Parsing Pipeline

For complex programming languages or DSLs, split parsing into two pure DCG passes:

1. **Lexer Pass**: `phrase(tokens(Tokens), InputChars)`
2. **Parser Pass**: `phrase(ast(AST), Tokens)`

---

## 6. Higher-Order DCGs (`call//N`) & Meta-Predicates

Avoid duplicating DCG rules just to vary an element non-terminal or predicate. Use `call//N` to parameterize grammar rules, and declare `:- meta_predicate` with `//` or `2` so closures resolve in the caller module context:

```prolog
:- module(seq_combinators, [
    seq_of//2
]).

:- meta_predicate
    seq_of(?, //, ?, ?).

% Generic DCG rule to match a list of elements using a parameter non-terminal nonterm//1
seq_of([], _) --> [].
seq_of([X|Xs], NonTerm) -->
    call(NonTerm, X),
    seq_of(Xs, NonTerm).

% Example usage with lambda or defined non-terminal
% phrase(seq_of(Xs, \C^([C], { char_type(C, digit) })), "123")
```

---

## 7. Execution Safety & Testing

Test DCG grammars with `testing.pl` or `plunit`:

```prolog
test(parse_addition) :-
    phrase(expr(AST), "1+2"),
    AST == bin_op(+, num(1), num(2)).
```
