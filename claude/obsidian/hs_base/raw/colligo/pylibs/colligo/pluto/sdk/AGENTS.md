# Agent Instructions: SDK

<!-- AGENTS:JUDGE:context START -->
## Context

- **Purpose:** <!-- TODO: 1–2 sentences describing what this does. -->
- **Key Files:**
  - `cli.py`
  - `pyproject.toml`
  - `__init__.py`
<!-- AGENTS:JUDGE:context END -->

<!-- AGENTS:JUDGE:technical_rules START -->
## Technical Rules

- **Distributable wheel** with its own `pyproject.toml`. Internal `colligo.pluto.*` deps are auto-bundled by `./pluto sdk validate-deps`.
- **Inherits Pluto-wide rules** (Python 3.12, absolute imports, ruff, mypy, copyright header).
- **Optional deps:** guard with `try/except ImportError` so the dep scanner skips them.
<!-- AGENTS:JUDGE:technical_rules END -->

<!-- AGENTS:JUDGE:common_commands START -->
## Common Commands

- **Validate deps:** `./pluto sdk validate-deps` (add `--fix` to auto-update)
- **Build wheel:** `./pluto sdk build`
- **Release:** `./pluto sdk release <major|minor|patch>`
- **Lint:** `./pluto lint`
- **Tests:** `pytest <path> -v`
<!-- AGENTS:JUDGE:common_commands END -->

<!-- AGENTS:JUDGE:dos_donts START -->
## Do's and Don'ts

- **DO:** keep public API and internals separated; import from `colligo.pluto.sdk` or its public submodules, never `_core`.
- **DO:** run `./pluto sdk validate-deps --fix` after adding/removing internal imports.
- **DON'T:** add an external PyPI dep without updating `pyproject.toml` and re-validating.
<!-- AGENTS:JUDGE:dos_donts END -->
