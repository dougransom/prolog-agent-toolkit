/** <module> agent_skills_dispatch
 *
 * Reusable pure Prolog agent skill dispatcher demonstrating homoiconic
 * skill registration, pure DCG query parsing, and safe goal dispatching.
 *
 * Compatible with Scryer Prolog, Trealla, SWI, and ISO Prolog systems.
 *
 * @author Doug Ransom
 * @license Unlicense
 */

:- module(agent_skills_dispatch, [
    agent_register_skill/2,
    agent_dispatch/3,
    agent_skill/2,
    run_demo/0
]).

:- use_module(library(lists), [member/2]).
:- use_module(library(dcgs)).
:- use_module(library(charsio), [format/2]).

% Homoiconic skill registry: skill(Name, Capabilities)
% Skills and capabilities are represented as pure Prolog facts.
:- dynamic(agent_skill/2).

agent_skill(calculator,   [arithmetic, evaluate, sum]).
agent_skill(text_analyst, [count_words, token_length, dcg_parse]).
agent_skill(validator,    [type_check, bounds_check]).

%% agent_register_skill(+SkillName:atom, +Capabilities:list) is det.
%  Dynamically registers a new capability bundle for the agent.
agent_register_skill(SkillName, Capabilities) :-
    assertz(agent_skill(SkillName, Capabilities)).

%% agent_dispatch(+Skill:atom, +Request:term, -Response:term) is semidet.
%  Dispatches a structured request to the corresponding skill handler.
agent_dispatch(calculator, add(X, Y), Result) :-
    Result is X + Y.
agent_dispatch(calculator, multiply(X, Y), Result) :-
    Result is X * Y.
agent_dispatch(text_analyst, word_count(Chars), Count) :-
    phrase(count_tokens(0, Count), Chars).
agent_dispatch(validator, in_range(Val, Min, Max), Valid) :-
    (   Val >= Min, Val =< Max ->
        Valid = valid
    ;   Valid = invalid
    ).

%% count_tokens(+Acc:integer, -Count:integer)// is det.
%  Pure DCG tokenizer counting whitespace-separated tokens.
count_tokens(Acc, Count) -->
    " ",
    !,
    count_tokens(Acc, Count).
count_tokens(Acc, Count) -->
    [C],
    { C \= ' ' },
    consume_token,
    { Acc1 is Acc + 1 },
    count_tokens(Acc1, Count).
count_tokens(Acc, Acc) --> [].

consume_token -->
    [C],
    { C \= ' ' },
    !,
    consume_token.
consume_token --> [].

%% run_demo is det.
%  Runs a self-contained demonstration of skill lookup and dispatch.
run_demo :-
    format("=== Prolog Agent Skill Dispatch Demo ===~n", []),
    agent_dispatch(calculator, add(40, 2), Ans1),
    format("1. Calculator add(40, 2) -> ~w~n", [Ans1]),
    agent_dispatch(text_analyst, word_count("pure ISO prolog agent"), Ans2),
    format("2. Text Analyst word_count('pure ISO prolog agent') -> ~w words~n", [Ans2]),
    agent_dispatch(validator, in_range(25, 0, 100), Ans3),
    format("3. Validator in_range(25, 0, 100) -> ~w~n", [Ans3]),
    format("Demo complete.~n", []).
