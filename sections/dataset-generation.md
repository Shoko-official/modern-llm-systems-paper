# Scientific Dataset Generation

## Methodology

Evaluating Retrieval-Augmented Generation (RAG) and agent runtimes requires high-quality, domain-specific evaluation datasets.
To construct these datasets from scientific publications, the architecture employs an LLM-powered extraction and synthesis pipeline.
This pipeline processes scientific text, isolates fact-based assertions (claims), synthesizes complex reasoning questions, and extracts precise citation snippets.

The dataset generator is registered as modular tools in the `AgentRuntime`, allowing execution telemetry to be fully captured, audited, and aligned under a single trace context.

```
┌───────────────────────────────────────────────────────┐
│              Dataset Generation Pipeline              │
│                                                       │
│   Document ──► extract_claims() ──► Factual Claims     │
│                     │                                 │
│                     ▼                                 │
│             synthesize_questions() ──► Q&A Pairs      │
│                     │                                 │
│                     ▼                                 │
│             format_qa_pair() ────► GeneratedDataset   │
│                                                       │
└───────────────────────────────────────────────────────┘
```

## Schema Standardization

The generated evaluation data conforms to a unified schema (`generated_dataset.json`).
Each Q&A record maps questions directly back to original text snippets and section headers:

```json
{
  "query_id": "QGEN-001",
  "query": "How are unsafe command executions prevented in the agent layer?",
  "answer": "The system addresses this by stating that: Memories are stored in a strict schema...",
  "citations": [
    {
      "document_id": "doc_retrieval_memory",
      "snippet": "Memories are stored in a strict schema...",
      "section": "Memory Layer Architecture"
    }
  ]
}
```

## Telemetry & Compliance

The orchestration pipeline logs spans for claim extraction and synthesis, yielding performance overhead statistics and ensuring all calls satisfy the repository's security governance filters.
For details on end-to-end telemetry and execution spans, refer to [Deployment and End-to-End Orchestration](deployment.md).
