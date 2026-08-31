# ADR 0001: Scryer Prolog as Primary Target Engine

- **Status**: Accepted
- **Date**: 2026-08-28

## Context
Prolog implementations vary significantly in their system features, handling of strings (`chars` vs strings vs lists of codes), constraint solver integration (`CLP(Z)` vs `CLP(FD)`), and logical purity (`library(reif)` reification vs non-logical cuts).

## Decision
We choose **Scryer Prolog** as the primary default target engine and baseline Prolog system for this toolkit.

## Rationale
1. **Purity & Modern Design**: Scryer Prolog emphasizes standard term semantics without non-standard default autoloading or mutable global state.
2. **Logical Purity First**: Scryer natively supports `library(reif)` (`if_/3`, `dif/2`), pure DCGs, and CLP(Z) out of the box.
3. **Rust Ecosystem & WASM Safety**: Scryer is written in Rust, offering strong memory safety and platform portability.

## Consequences
- All standard module templates created by `prolog-agent init` default to Scryer Prolog (`bakage.toml` manifest, `library(charsio)`, `library(dcgs)`).
- Standards for SWI, Trealla, and Tau remain supported as explicit opt-in target Prolog systems.
