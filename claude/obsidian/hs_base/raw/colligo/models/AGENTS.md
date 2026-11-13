# models

## Conventions

- Treat `models/` as many independent package roots, not one uniform subsystem. Each package has its own `colligo.yaml`, `build.py`, and co-located `tests/` directory.

## Common Pitfalls


- Check whether a package uses `custom_pyenv` in `colligo.yaml` before changing dependencies or runtime assumptions.
- Keep package metadata, implementation code, endpoint/worker registration, and tests aligned in the same change.

