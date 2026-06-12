# Modern LLM Systems 2026 Paper

`modern-llm-systems-paper` is the paper workspace for the Modern LLM Systems 2026 / arXiv Report program.

This repository will contain the report source, paper structure, citation flow, reproducible figures, and paper validation once those items are introduced by dedicated issues.

It is not a research ledger, benchmark repository, RAG prototype, inference lab, or agent runtime.

## Repository Role

This repository owns:

* paper governance rules;
* paper structure when introduced;
* citation readiness rules;
* figure and diagram policy;
* paper-specific validation;
* final report assembly once the required foundations exist.

The central project board is:

* [Modern LLM Systems 2026 / arXiv Report](https://github.com/users/Shoko-official/projects/4)

## Current Scope

Milestone 0 is limited to governance.

Included:

* governance documentation;
* issue and MR/PR templates;
* minimal validation commands;
* minimal CI;
* initial paper folder structure.

Out of scope:

* scientific section drafting;
* real bibliography entries;
* generated figures;
* full LaTeX build setup;
* final arXiv packaging;
* RAG, inference, memory, agents, or GraphRAG implementation.

## Citation Policy

Scientific and technical claims must be traceable to the research ledger or explicitly marked as unresolved.

Paper-ready claims should have:

* a source reference;
* an evidence status;
* citation readiness;
* no unresolved `TODO:evidence_needed` marker.

Unverified claims must not be presented as final conclusions.

## Figure Policy

Allowed source formats:

* Mermaid text diagrams for workflows, system architecture, state diagrams, dependency graphs, and concept maps.
* Python-generated images for quantitative charts, visual tables, and figures that are not practical in Mermaid.

Not allowed by default:

* web images;
* screenshots unless explicitly approved;
* hand-drawn images;
* Figma, Canva, or PowerPoint exports;
* manually authored complex SVGs;
* binary figures without a clear source;
* orphan figures that are not referenced by the paper or documentation.

Temporary Python scripts used to generate images must be deleted after generation unless a dedicated issue approves keeping them under `scripts/figures/` for reproducibility.

Important paper figures may keep their Python generation script under `scripts/figures/` when the issue explicitly requires long-term reproducibility.

## License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
