:- use_module(library(format)).
:- use_module(library(dcgs)).
:- use_module('../src/starter_project.pl').

:- initialization(run_tests).

run_tests :-
    hello(Msg),
    format("Test hello/1 passed: ~s~n", [Msg]),
    (   phrase(parse_item("abc"), "[abc]") ->
        format("Test parse_item//1 passed.~n", [])
    ;   format("Test parse_item//1 failed!~n", []),
        halt(1)
    ).
