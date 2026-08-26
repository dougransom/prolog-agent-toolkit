---
name: prolog-packaging
description: Guidelines and manifest standards for packaging and dependency management in Prolog (Scryer bakage, SWI pack_install).
---

# Prolog Packaging Standards

Use this skill when initializing package manifests, managing dependencies, or preparing Prolog libraries for distribution.

## Scryer Prolog Packaging (`bakage`)

For Scryer Prolog projects, use [`bakage`](https://github.com/bakaq/bakage) packaging conventions.

### `pack.pl` / Manifest Format
Define package details in a standard manifest `pack.pl`:
```prolog
name(my_scryer_lib).
version('0.1.0').
title("My Scryer Prolog Library").
author("Author Name").
home("https://github.com/user/my_scryer_lib").
dependencies([
    testing
]).
```

### Installing Dependencies with `bakage`
Run `bakage` to fetch dependencies:
```bash
bakage install
```

---

## SWI-Prolog Packaging (`pack`)

For SWI-Prolog projects, define a `pack.pl` manifest:
```prolog
name('my_swi_lib').
version('0.1.0').
title('My SWI-Prolog Library').
keywords(['prolog', 'utility']).
author('Author Name', 'author@example.com').
home('https://github.com/user/my_swi_lib').
download('https://github.com/user/my_swi_lib/releases/*.zip').
```

### Installing Packs
```bash
swi-safe -g "pack_install(my_swi_lib),halt"
```

---

## Tau Prolog Packaging (`npm`)

For Tau Prolog projects (Node.js and Web/DOM), use `npm` package manager with `package.json`:

```json
{
  "name": "my-tau-prolog-app",
  "version": "1.0.0",
  "description": "Tau Prolog embedded application",
  "main": "index.js",
  "dependencies": {
    "tau-prolog": "^0.3.4"
  }
}
```

### Installing Dependencies
```bash
npm install tau-prolog
```

