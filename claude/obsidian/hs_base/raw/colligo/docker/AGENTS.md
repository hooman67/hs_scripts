# docker

Container images for local development (`docker/dev`, `docker/dev2_0`) and deployed inference (`docker/rhode-deploy`). These are separate products; never treat them as interchangeable.

## Commands

- Dev image: `docker/dev/make.py` with subcommands `build`, `run`, `start`, `stop`, `attach`, `push`
- Dev2_0 image: `docker/dev2_0/make.py` with subcommands `build`, `run`, `start`, `stop`, `attach`, `push`
- Deploy image: `docker/rhode-deploy/Makefile` with targets `cpu`, `gpu`, `push-cpu`, `push-gpu`

## Release notes — MANDATORY

**CI will fail** (the release notes check in CI) whenever the workflow's `on.pull_request.paths` filter matches your changes but `aidoc/inference-platform/support/release.md` was not updated.

The path filter excludes `*.md` files under each docker subdirectory, so documentation-only changes do not trigger the check and need no bump.

Before opening a PR that touches non-doc files in `docker/`, check whether your changes match those path filters. If they do, you MUST:

1. Bump the version in `docker/VERSION` using **patch** or **minor** only (see below).
2. Prepend a new entry to `aidoc/inference-platform/support/release.md`.

Run the `prepare-release` skill (Claude Code) or `tools/prepare-release.py` to do both steps correctly.

### Which bump type to use

**patch** — fixes and remediations that don't add capability:
- Fix a broken install step (e.g. switching a PPA to an official apt feed)
- CVE remediation or security patch

**minor** — new capability or compatible dependency upgrade:
- Add a new tool or SDK to the image
- Upgrade a dependency to a newer compatible version

**NEVER do a major bump.** Major versions represent whole new image generations (e.g. `docker/dev` is v1, `docker/dev2_0` is v2). These are architectural decisions made by humans, not incremental changes.

## Boundaries

- NEVER change base images, system packages, or publishing behavior without checking existing docs and release flow.
