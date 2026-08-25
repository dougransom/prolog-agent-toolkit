Prefer prolog code with [logical purity properties](https://www.metalevel.at/prolog/purity). Included in this are:
- prefer if_ and the predictes from reif.
- prefer clpz and clpb over impure built in predicates.

Use [Scryer Prolog](https://www.scryer.pl/) language and library documentation.
Tests use [Testing](https://github.com/bakaq/testing.pl).
Packages use [Bakage](https://github.com/bakaq/bakage).

Use any packages referenced in our project.

Look for opportunities to use DCGs.  

When relating condition to a value, then doing something further with that value, prefer an approach that isolates the test<->value relation. i.e. if_(G,A="A",A="B"), write(A) rather than writing A in each branch.

Avoid repetition of code, use prolog expansion mechanisms or assert type statements.

Use logging for diagnostics meant to be left in and activated at runtime.

See the guidelines in [Covington](covington_style.md).
