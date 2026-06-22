# System Layers

Draft status: Drafted.

Purpose: Organize the major layers of modern LLM systems.

Evidence requirement: Layer descriptions added later must be backed by approved
ledger claims and sources.

## Core System Layers

* **Model and Training Layers**: Covers the neural network architecture (specifically the self-attention mechanism [@source-attention-2017]) and model parameters adaptation (pre-training, supervised fine-tuning, and alignment).
* **Inference and Serving**: Manages serving runtimes, dynamic batching scheduling, and KV Cache paging optimizations (such as PagedAttention [@source-kv-cache-2023]) to enhance token generation throughput.
* **Retrieval and Memory**: Handles retrieval-augmented generation (RAG) chunking pipelines, dense/sparse search indexing, and conversational history cache retention.
* **Agents and Tool Use**: Integrates reasoning planners, goal routers, and tools executors to perform structured task execution loops.
* **Governance and Security**: Implements client-facing gatekeepers, input safety filters to intercept prompt injections [@source-adversarial-2024], and sandboxed execution boundaries.
* **Observability and Evaluation**: Collects system execution traces represented as trees of spans [@source-dapper-2010], aggregates metrics, and computes evaluation dataset scores.

This section presents the multi-layered stack of modern LLM systems, spanning from hardware acceleration up to orchestrators and agents.
