---
name: prolog-packaging
description: Guidelines and manifest standards for packaging and dependency management in Prolog (Scryer bakage, SWI pack_install).
---

# Prolog Packaging Standards

Use this skill when initializing package manifests, managing dependencies, or preparing Prolog libraries for distribution.

## Scryer Prolog Packaging (`bakage`)

For Scryer Prolog projects, use [`bakage`](https://github.com/bakaq/bakage) packaging conventions.

### Manifest Formats (`bakage.toml` or `pack.pl`)

`bakage` supports standard `bakage.toml` metadata:
```toml
name = "my_scryer_lib"
version = "0.1.0"
modules = ["src/my_scryer_lib.pl"]
requires = []
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

## Makefile Packaging Targets (`make packages`)

Projects can include optional packaging recipes in their `Makefile` to build release archives for all configured package managers:

```makefile
.PHONY: packages package_bakage package_swi package_npm package_python

# Aggregate target: Builds release artifacts for all configured package managers
packages: test docs package_bakage package_swi

# 1. Scryer Prolog bakage archive
package_bakage:
	@echo "=== Building Scryer bakage package ==="
	mkdir -p dist
	tar -czvf dist/$(NAME)-$(VERSION)-bakage.tar.gz bakage.toml pack.pl README.md LICENSE src/ tests/

# 2. SWI-Prolog pack archive
package_swi:
	@echo "=== Building SWI pack_install package ==="
	mkdir -p dist
	zip -r dist/$(NAME)-$(VERSION)-swi.zip pack.pl prolog/ README.md LICENSE

# 3. Tau Prolog / npm package
package_npm:
	@echo "=== Building npm package ==="
	npm pack --pack-destination=dist/

# 4. Python FFI / CLI package (if applicable)
package_python:
	@echo "=== Building Python wheel and sdist ==="
	uv build --out-dir dist/
```


