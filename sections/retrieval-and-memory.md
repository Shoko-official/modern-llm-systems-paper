# Retrieval and Memory

Draft status: Drafted.

Purpose: Reserve space for retrieval, grounding, and memory-related systems.

Evidence requirement: Future content must separate retrieval evidence, memory
claims, and unresolved notes.

## Retrieval Infrastructure & Grounding

The retrieval layer leverages an Abstract Syntax Tree (AST) chunker to parse raw programming modules into structural code snippets, ensuring high semantic consistency. Retrieval is executed via a hybrid search pipeline that fuses sparse term-frequency statistics (TF-IDF/BM25) and dense character-level n-gram cosine similarities. Results from both retrieval mechanisms are fused using either linear combinations or Reciprocal Rank Fusion (RRF), followed by a customized reranking stage utilizing lexical boosts and structural boosts (e.g., class vs function type weights).

Context grounding propagation ensures that all retrieved documents are validated against the session permission Access Control Lists (ACLs) to prevent unauthorized information disclosure.

## Memory Layer Architecture

The memory layer manages stateful long-term and short-term conversational context across user sessions. Memories are stored in a strict schema enforcing metadata tracing, temporal boundaries, and explicit data governance:

1. **Provenance Tracking**: Every conversational memory is tagged with its session lineage and source document IDs, maintaining context validity.
2. **Temporal Boundaries (TTL)**: Memory entries carry a creation timestamp and a configurable Time-To-Live (TTL). Expired entries are automatically pruned and denied from subsequent query processing.
3. **Explicit Revocation**: To ensure privacy and regulatory compliance (e.g., GDPR), memory records can be explicitly revoked by the user, permanently deleting them from the storage index.

## Memory Provenance & Expiry

<!-- MEMORY_STATS_START -->
<!-- MEMORY_STATS_END -->

