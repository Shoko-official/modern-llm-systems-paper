# References

This directory is reserved for paper-side reference material.

The research ledger is the source of evidence readiness. This directory should
only hold paper-facing reference artifacts once the handoff rules are clear.

The current placeholder index is `index.md`, and the bibliography placeholder is `bibliography.bib`.

## Expected Role

Future files in this directory may contain:

* bibliography files;
* citation notes for paper sections;
* mappings from ledger source IDs to paper references;
* citation readiness checks.

## Citation Handoff

Paper drafting should start from ledger records, not raw links.

A paper citation candidate should identify:

* the ledger claim ID being used;
* the ledger source ID or source IDs supporting that claim;
* whether the source is primary or secondary;
* whether the claim is ready for paper prose;
* any remaining missing citation details.

## Readiness States

Use these paper-side states when tracking citation work:

| State | Meaning |
|---|---|
| `ready_for_bibliography` | Ledger source record is complete enough to become a paper reference. |
| `missing_citation_detail` | Evidence exists, but the paper still needs a locator, BibTeX entry, or similar reference detail. |
| `missing_evidence` | Claim does not yet have enough support for paper use. |
| `blocked` | Source or claim status prevents use in paper prose. |

Missing evidence and missing citation detail are different states. Missing
evidence blocks the claim. Missing citation detail blocks final reference work
but may still allow planning notes.

## Paper Drafting Rules

Do not introduce paper prose from a ledger claim unless the claim is marked as a
paper candidate or ready in the ledger.

Do not convert raw URLs into paper references before a source record exists in
the ledger.

Do not add final bibliography entries from this handoff issue.

## Current Limits

Do not add real bibliography entries, citation commands, or paper-ready citation
lists from this handoff issue.

The reference index is not a bibliography and should remain empty until a
dedicated issue introduces paper-facing entries from approved ledger sources.
