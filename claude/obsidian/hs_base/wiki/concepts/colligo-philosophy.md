---
type: concept
title: Colligo Monorepo Philosophy
tags: [colligo, philosophy, monorepo, software-engineering]
created: 2026-07-04
updated: 2026-07-04
sources: ["[[raw/colligo/aidoc/philosophy.md]]"]
---

# Colligo Monorepo Philosophy

The design rationale behind [[wiki/entities/colligo|Colligo]] being one monorepo rather than many repos — pinned as `whoami` at the top of the docs site.

## Mission

The AI platform exists to facilitate the **end-to-end lifecycle of delightful AI experiences** for Adobe users — inference, training, and data processing, some self-serve, some not. It formed by merging three earlier efforts: inference tech for Firefly generative services, data processing for training Firefly models, and the AI compute platform.

## Two code lifecycles

Borrowing Google's "programming vs software engineering" framing:

- **Short-lived code** (research/prototyping, days–months): software-engineering rigor is overhead. Delivered as **installable packages** (pip / `adobe-aip`), matching community tools (Flyte, MLflow, Metaflow, Ray). See [[wiki/concepts/colligo-inference-sdk|the Inference SDK]].
- **Long-lived code** (production, evolves for years): rigor is mandatory. Goal — **as code grows, collective maintenance overhead grows sublinearly**. Code is a liability; keep it minimal.

## Why a monorepo for long-lived code

Software is a *network* of interdependent code across many teams. Separate repos per team look locally optimal but, once teams move fast and depend on each other, cause: (a) cross-team changes forcing everyone to learn every team's tools, and (b) one team silently breaking another's code that's only discovered on a lazy update — "dependency hell."

A monorepo **with proper tooling and processes** gives every team a uniform build/test/lint ecosystem and the ability to test all code together as changes land, while minimizing per-team overhead (never zero — it's not a zero-sum game). This underpins Colligo's single-version dependency policy and shared `./m` tooling (see [[wiki/concepts/colligo-dev-workflow]], [[wiki/concepts/colligo-architecture]]).

The current tooling has scaled to ~200 developers and is being reworked (FFP-14611) for the next phase of scaling.

## Related

- [[wiki/entities/colligo]]
- [[wiki/concepts/colligo-architecture]]
- [[wiki/concepts/colligo-dev-workflow]]
