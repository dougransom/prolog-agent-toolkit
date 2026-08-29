---
name: prolog-packaging
description: Guidelines and manifest standards for packaging and dependency management in Prolog (Scryer bakage, SWI pack_install).
---

# Prolog Packaging Standards

Use this skill when initializing package manifests, managing dependencies, or preparing Prolog libraries for distribution.

## Scryer Prolog Packaging (`bakage`)

For Scryer Prolog projects, use [`bakage`](https://github.com/bakaq/bakage) packaging conventions.

### Manifest Formats (`scryer-manifest.pl` or `pack.pl`)

`bakage` uses Prolog term facts in `scryer-manifest.pl`:
```prolog
name("my_scryer_lib").
version("0.1.0").
main_file("src/my_scryer_lib.pl").
dependencies([]).
```

Or classic `pack.pl` manifest:
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

---

## Packaging & Archive Validation CLI (`prolog-agent pack`)

Use `prolog-agent pack` to validate manifests (`bakage.toml`, `pack.pl`, `package.json`), verify that all declared module source files exist, and build clean release archives:

```bash
# Build Scryer bakage tar.gz archive
prolog-agent pack --engine scryer

# Build SWI pack zip archive
prolog-agent pack --engine swi
```

---

## Makefile Packaging Targets (`make packages`)

Projects can include packaging recipes in their `Makefile` leveraging `prolog-agent pack`:

```makefile
.PHONY: packages package_bakage package_swi package_npm package_python

# Aggregate target: Builds release artifacts for configured package managers
packages: test package_bakage package_swi

# 1. Scryer Prolog bakage archive
package_bakage:
	@echo "=== Building Scryer bakage package ==="
	prolog-agent pack --engine scryer

# 2. SWI-Prolog pack archive
package_swi:
	@echo "=== Building SWI pack_install package ==="
	prolog-agent pack --engine swi

# 3. Tau Prolog / npm package
package_npm:
	@echo "=== Building npm package ==="
	npm pack --pack-destination=dist/

# 4. Python FFI / CLI package (if applicable)
package_python:
	@echo "=== Building Python wheel and sdist ==="
	uv build --out-dir dist/
```


