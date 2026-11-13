# Foundry Studio

The Studio Product work area. Contains all code for the Foundry Studio web application and its supporting infrastructure.

## 1. Packages

| Package | Description |
|---|---|
| `web/` | Lit + TypeScript frontend |
| `backend/` | NestJS CRUD API for the web app |
| `colligo-contracts/` | Shared Colligo contract library (consumed by backend and web) |
| `terraform/` | AWS infrastructure for Studio (corp, prod, stage environments) |
| `uxp/` | UXP plugin for Foundry Studio in DVA apps |

See each package's `README.md` and `AGENTS.md` for details.

## 2. Development Setup

### 2.1 VS Code

The `.vscode/` directory lives in `foundry-studio/`, not the repo root. Open `foundry-studio/` as your workspace folder in VS Code (or add it as a folder in a multi-root workspace) to get launch configs and tasks.

### 2.2 Prerequisites

- `pnpm` — package manager for all TS projects. Install via `npm install -g pnpm`.
- `nvm` — Node version manager (required for `web/`; see `web/AGENTS.md`).
- `docker` — for local backend dev. Request a license via [Support Center](https://adobe.service-now.com/esc?id=adb_esc_search#q=docker&t=All).
- `helm`, `aws` (CLI), `terraform`, `kubectl` — as needed for deployment and ops tasks.

### 2.3 Pre-commit Hooks

This package uses [Husky](https://typicode.github.io/husky/) and [lint-staged](https://github.com/lint-staged/lint-staged) to run linting on staged files before each commit.

**Setup** (automatic on first `pnpm install`):

```bash
cd foundry-studio
pnpm install
# Husky hooks are installed automatically via the "prepare" script
```

**Adding your project to pre-commit hooks:**

1. Add `lint`, `lint:fix`, and `lint:staged` scripts to your `package.json`.
2. Add your project's glob pattern to `.lintstagedrc.mjs`.

```javascript
// .lintstagedrc.mjs
'your-project/**/*.{ts,tsx,js,jsx}': (filenames) => {
  const files = getRelativeFiles(filenames, 'your-project');
  return `pnpm -C your-project lint:staged ${files}`;
},
```

**Troubleshooting:**

```bash
# Hooks not running? Reinstall:
pnpm install

# Test a hook manually:
pnpm lint:staged src/file-that-changed.ts
```
