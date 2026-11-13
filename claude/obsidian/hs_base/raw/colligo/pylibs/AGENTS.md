# pylibs

## Boundaries

- NEVER treat all of `pylibs/` as one package or assume `pluto`, `rhode`, `fastapi`, `repo`, and `base` follow the same workflow.

## Conventions

- Work package by package. Start with the nearest `colligo.yaml` and co-located `tests/` directory for the package you are editing. Treat package-local `colligo.yaml` as the source of truth for dependencies, visibility, and custom env selection; `pylibs/pyproject.toml` and generated env project files are not.

- `pylibs/colligo/pluto/dashboard` is a separate frontend workflow with its own `package.json` scripts (`dev`, `test`, `lint`, `build:proto:dev`, `build`). Use those instead of Python commands, and regenerate proto/types via the package scripts rather than hand-editing `_generated/`.
