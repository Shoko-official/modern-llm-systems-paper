# Contributing

This repository uses small, reviewable changes tied to GitHub issues. Paper changes must remain traceable to research evidence and reproducible assets.

## Language

Repository artifacts must be written in English unless a dedicated issue explicitly requires another language.

## Workflow

Every change must follow this sequence:

1. Start from an existing issue.
2. Summarize the objective, scope, files, risks, validation commands, and estimated MR/PR size.
3. Create a local branch from `main`.
4. Make local changes only.
5. Run the narrowest relevant checks.
6. Review the diff locally.
7. Present the diff for review.
8. Wait for explicit approval before pushing unless the issue has already granted a narrower exception.
9. Push the branch only after approval.
10. Open an MR/PR linked to the issue.
11. Wait for CI when CI exists.
12. Request final approval before merge unless the issue has already granted a narrower exception.

Direct work on `main` is forbidden after repository bootstrap.

## Branch Naming

Use one of these branch patterns:

* `docs/paper/<issue-id>-short-name`
* `feat/paper/<issue-id>-short-name`
* `fix/paper/<issue-id>-short-name`

Examples:

* `docs/paper/1-governance-docs`
* `docs/paper/2-paper-templates`
* `feat/paper/3-minimal-validation`

## Paper Rules

Do not add scientific content during Milestone 0.

When paper content is introduced later:

* every factual claim must be traceable to the research ledger or marked unresolved;
* claims without evidence must be marked `TODO:evidence_needed`;
* citations must not be invented;
* unresolved placeholders must remain visible;
* paper-ready content must not depend on private or non-redistributable data.

## Issue Closing Rules

Use closing keywords only when the MR/PR fully completes the issue:

* `Closes #123`
* `Fixes #123`
* `Resolves #123`

Use non-closing references when the MR/PR is partial:

* `Refs #123`
* `Related to #123`
* `Part of #123`

Never invent an issue number. Create the issue first or ask for confirmation.

## Figure Rules

Allowed source formats:

* Mermaid text files or Mermaid blocks.
* Python-generated image outputs.

External images, screenshots, manual drawings, and design-tool exports require explicit approval.

Temporary Python scripts used to generate images must be deleted after generation unless a dedicated issue approves keeping them under `scripts/figures/` for reproducibility.

Important paper figures may keep their Python generation script under `scripts/figures/` only when the issue explicitly requires it.

Figure files must have clear names, such as:

* `figures/system_stack_overview.png`
* `figures/rag_pipeline.mmd`
* `figures/kv_cache_memory_curve.png`

Names such as `image1.png`, `test.png`, `final_final.png`, or `diagram_ok.png` are not acceptable for committed paper figures.

## Review Rules

Before presenting a diff, verify:

* the issue scope is respected;
* no scientific content is added before the relevant issue;
* citations are present or unresolved markers remain visible when citation work is in scope;
* figures follow the allowed source policy when figure work is in scope;
* no private data is present;
* no secret, token, credential, or sensitive log is present;
* validation commands were run or a clear reason is documented.

## Validation

Milestone 0 will introduce the standard commands:

```bash
make validate
make lint
make test
```

Until the Makefile exists, document that these commands are not yet available and run the checks that are possible for the current issue.
