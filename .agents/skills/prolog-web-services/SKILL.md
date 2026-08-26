---
name: prolog-web-services
description: Guidelines for building HTTP REST APIs, JSON endpoints, microservices, and WebSockets in Prolog. Use when exposing Prolog predicates over web HTTP interfaces.
---

# Prolog Web Services & HTTP API Guidelines

Use this skill when building HTTP REST APIs, microservices, or JSON web endpoints directly in Prolog.

## 1. Engine Web Frameworks

### SWI-Prolog HTTP Dispatcher
```prolog
:- use_module(library(http/thread_http_server)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).

:- http_handler(root(api/solve), solve_handler, []).

server(Port) :-
    http_server(http_dispatch, [port(Port)]).

solve_handler(Request) :-
    http_read_json_dict(Request, DictIn),
    % Perform logic...
    reply_json_dict(_{status: "success", result: [1, 2, 3]}).
```

### Scryer Prolog HTTP Server & Client
```prolog
:- use_module(library(http/http_open)).

fetch_url(URL, Content) :-
    http_open(URL, Stream, []),
    get_char(Stream, Char),
    % Read stream contents into chars list...
    close(Stream).
```

---

## 2. JSON Serialization Standards

- Represent JSON objects in ISO Prolog as terms or character lists (`chars`).
- Keep request validation pure by parsing incoming payloads via DCGs (`phrase(json_ast(AST), Chars)`).

---

## 3. Microservice Architecture & Safety

- Run Prolog HTTP microservices behind a reverse proxy (e.g. Nginx, Caddy, or Envoy).
- Apply system resource quotas and timeouts via `prolog-safe`.
