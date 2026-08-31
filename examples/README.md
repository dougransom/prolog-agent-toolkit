# Prolog Agent Toolkit Examples

This directory contains canonical, runnable examples demonstrating core patterns for building AI agents, Model Context Protocol (MCP) servers, skill dispatchers, and neurosymbolic verifiers in pure ISO Prolog.

## Examples Overview

| File | Purpose | Key Standards & Libraries |
|---|---|---|
| [`agent_skills_dispatch.pl`](agent_skills_dispatch.pl) | Homoiconic agent skill registry and pure DCG request routing | Pure DCGs, `library(charsio)`, `library(lists)` |
| [`prolog_mcp_server.pl`](prolog_mcp_server.pl) | Model Context Protocol (MCP) JSON-RPC tool server pattern | Tool schema definitions, structured result terms |
| [`neurosymbolic_reasoner.pl`](neurosymbolic_reasoner.pl) | Deterministic ground-truth proof engine verifying LLM claims & constraints | `library(clpz)`, pure relational knowledge bases |

---

## Running the Examples

All examples are portable across Scryer Prolog, Trealla, and SWI-Prolog. Run them safely using the toolkit's sandboxed runners:

### 1. Agent Skill Dispatcher
```bash
scryer-safe -g "use_module('examples/agent_skills_dispatch.pl'), agent_skills_dispatch:run_demo, halt."
# Or with generic runner:
PROLOG_ENGINE=scryer prolog-safe -g "use_module('examples/agent_skills_dispatch.pl'), agent_skills_dispatch:run_demo, halt."
```

### 2. Prolog MCP Server
```bash
scryer-safe -g "use_module('examples/prolog_mcp_server.pl'), prolog_mcp_server:run_demo, halt."
```

### 3. Neurosymbolic Constraint & Proof Engine
```bash
scryer-safe -g "use_module('examples/neurosymbolic_reasoner.pl'), neurosymbolic_reasoner:run_demo, halt."
```
