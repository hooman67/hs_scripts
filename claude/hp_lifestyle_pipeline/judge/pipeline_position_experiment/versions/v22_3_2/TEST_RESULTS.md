# V22.3.2 offline verification

- Runtime: CPython 3.12.11
- Command: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv312/bin/python -m pytest tests -q -p no:cacheprovider`
- Result: **156 passed in 35.14s**
- Command: `.venv312/bin/ruff check --select F,E9,I hp3p tests`
- Result: **All checks passed**
- Command: `git diff --check`
- Result: **passed**
