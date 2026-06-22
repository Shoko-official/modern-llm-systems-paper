# Introduction

Draft status: Drafted.

Purpose: Define the paper scope, audience, and motivating questions.

Evidence requirement: Any technical motivation added later must link back to
approved ledger claims and sources.

In recent years, the adoption of Large Language Models (LLMs) has transitioned from standalone prototype models to complex, multi-layered production systems. The core architecture of these systems is built upon the Transformer model [@source-attention-2017], which introduced the self-attention mechanism to enable parallel token processing. Ranging from training adaptation to runtime inference serving, modern LLM systems require deep co-design across hardware platforms, software runtime executors, and safety guardrails.

## Paper Scope

* **Systems Focus**: Multi-layered LLM system architecture, including execution runtimes, memory caches, and agent coordinators.
* **Component Boundaries**: Rigorous boundaries separating model parameter adaptation, RAG search indices, distributed serving simulators, and observability exporters.

## Target Audience

* **System Architects**: Engineers designing high-performance LLM runtimes and agent coordinators.
* **Researchers**: Computer scientists analyzing optimization tradeoffs in serving memory and security policies.

## Motivating Questions

* **Scalability**: How do serving infrastructures partition model weights and KV caches to handle high concurrency?
* **Security**: What defense mechanisms exist to filter prompt injections and enforce access control policies at the system boundaries?

This paper surveys the architectural choices, tradeoffs, and metrics defining modern LLM systems in 2026.
