# tools

## Conventions

- Some task names in `tools/tasks.py` exist only for docs visibility, while `./m` dispatches to a different implementation. Check the function body before assuming a command is the real execution path.
- NEVER introduce a parallel wrapper if an equivalent `./m` or `tools/*` entrypoint already exists.

## Key files

| File | Purpose |
|------|---------|
| `tools/env.py` | Environment-management entrypoints |
| `tools/uv.sh` | UV bootstrap and dependency helper script |
