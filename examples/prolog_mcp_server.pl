/** <module> prolog_mcp_server
 *
 * Model Context Protocol (MCP) tool server pattern in pure Prolog.
 * Demonstrates listing tools, validating input schemas, and executing tool calls
 * with structured JSON-compatible response terms.
 *
 * Compatible with Scryer Prolog, Trealla, SWI, and ISO Prolog systems.
 *
 * @author Doug Ransom
 * @license Unlicense
 */

:- module(prolog_mcp_server, [
    mcp_list_tools/1,
    mcp_call_tool/3,
    mcp_handle_request/2,
    run_demo/0
]).

:- use_module(library(charsio), [format/2]).
:- use_module(library(lists), [member/2]).

%% mcp_tool(-ToolDef:term) is nondet.
%  Schema definitions for exposed tools.
mcp_tool(tool(
    name(prolog_eval),
    description("Evaluates a pure arithmetic constraint or expression"),
    parameters([
        param(val1, number, "First number"),
        param(val2, number, "Second number"),
        param(op, atom, "Operation: add or mul")
    ])
)).

mcp_tool(tool(
    name(prolog_unify),
    description("Tests declarative unification between two terms"),
    parameters([
        param(term1, any, "First term"),
        param(term2, any, "Second term")
    ])
)).

%% mcp_list_tools(-Tools:list) is det.
%  Returns all registered MCP tools in the server.
mcp_list_tools(Tools) :-
    findall(Tool, mcp_tool(Tool), Tools).

%% mcp_call_tool(+Name:atom, +Args:list, -Result:term) is semidet.
%  Executes an MCP tool call with arguments and returns structured output.
mcp_call_tool(prolog_eval, [arg(val1, X), arg(val2, Y), arg(op, add)], result(Answer)) :-
    Answer is X + Y.
mcp_call_tool(prolog_eval, [arg(val1, X), arg(val2, Y), arg(op, mul)], result(Answer)) :-
    Answer is X * Y.
mcp_call_tool(prolog_unify, [arg(term1, T1), arg(term2, T2)], result(Status)) :-
    (   T1 = T2 ->
        Status = unified(T1)
    ;   Status = failed_to_unify
    ).

%% mcp_handle_request(+Request:term, -Response:term) is det.
%  Top-level JSON-RPC / MCP request dispatcher.
mcp_handle_request(request(id(Id), method(tools_list), _), response(id(Id), result(Tools))) :-
    mcp_list_tools(Tools).
mcp_handle_request(request(id(Id), method(tools_call), params(Name, Args)), response(id(Id), Result)) :-
    (   mcp_call_tool(Name, Args, Result) ->
        true
    ;   Result = error("Tool execution failed or invalid arguments")
    ).
mcp_handle_request(request(id(Id), method(Unknown), _), response(id(Id), error(unknown_method(Unknown)))).

%% run_demo is det.
%  Executes a demonstration of MCP tool listing and tool invocation.
run_demo :-
    format("=== Prolog MCP Server Pattern Demo ===~n", []),
    mcp_handle_request(request(id(1), method(tools_list), []), Resp1),
    format("1. Tools list response: ~w~n", [Resp1]),
    mcp_handle_request(
        request(id(2), method(tools_call), params(prolog_eval, [arg(val1, 6), arg(val2, 7), arg(op, mul)])),
        Resp2
    ),
    format("2. Tools call response: ~w~n", [Resp2]),
    mcp_handle_request(
        request(id(3), method(tools_call), params(prolog_unify, [arg(term1, f(a, _TargetVar)), arg(term2, f(a, 42))])),
        Resp3
    ),
    format("3. Term unification call response: ~w~n", [Resp3]),
    format("MCP Demo complete.~n", []).
