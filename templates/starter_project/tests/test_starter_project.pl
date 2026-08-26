:- use_module(library(plunit)).
:- use_module('../src/starter_project.pl').

:- begin_tests(starter_project).

test(hello) :-
    hello(Msg),
    assertion(Msg \== []).

test(dcg_parse) :-
    phrase(parse_item("test"), "[test]").

:- end_tests(starter_project).
