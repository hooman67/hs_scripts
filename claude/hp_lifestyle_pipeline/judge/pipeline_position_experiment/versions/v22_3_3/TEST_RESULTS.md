# V22.3.3 offline verification

- Runtime: CPython 3.12.11
- Full pytest: **166 passed in 35.63s**
- Ruff (`F,E9,I`): **all checks passed**
- `git diff --check`: **passed**
- Regression coverage includes exact benign Astra sentence cleanup, negated fixed-position wording, active move/relocate/translate commands, fixed-writer contradiction rejection, bounded Stage-B/image calls and HIGH-FILL unchanged behavior.
