:- module(starter_project, [
    hello/1,
    parse_item//1,
    solve_range/2
]).

:- use_module(library(charsio)).
:- use_module(library(dcgs)).
:- use_module(library(clpz)).
:- use_module(library(reif)).

%%  hello(-Greeting:chars) is det.
%   Generates standard greeting string.
hello("Hello from starter_project!").

%%  parse_item(-Item:chars)// is det.
%   Pure DCG rule for parsing an item tag.
parse_item(Item) -->
    "[", Item, "]".

%%  solve_range(+N:integer, -X:integer) is semidet.
%   CLP(Z) integer constraint example.
solve_range(N, X) :-
    X #>= 0,
    X #=< N,
    X #= N - 1.
