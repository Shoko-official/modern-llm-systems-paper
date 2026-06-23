# Deployment and End-to-End Orchestration

## Orchestrator Architecture

The pipeline orchestrates components across memory, search (RAG), safety governance, and execution layers in a synchronized environment. The interaction sequence aligns all spans under a single distributed trace.

```
[User Request] 
      │
      ▼
┌──────────────┐      ┌────────────────┐      ┌──────────────┐
│ AgentRuntime ├─────►│ SecurityFilter ├─────►│  Telemetry   │
│  (Orchestrate)│      │   (Governance) │      │  (Collector) │
└──────┬───────┘      └────────────────┘      └──────┬───────┘
       │                                             ▲
       ├─────► [RAG Searcher] ───────────────────────┤
       │                                             │
       └─────► [Memory Manager] ─────────────────────┘
```

## Performance & Integration Telemetry

Below is the consolidated performance data captured from the deployment pipeline.

### Latency Profiles by Service

| Service / Layer | Average Latency |
| :--- | :--- |
| Memory | 0.333 ms |
| Rag | 0.999 ms |
| Security | 0.000 ms |
| Agent-runtime | 0.650 ms |

### Security Auditing Summary

| Telemetry Dimension | Capture Metric |
| :--- | :--- |
| **Trace ID** | `266da896eafb48548dbbdc4755d1e5bb` |
| **Total Captured Spans** | `40` |
| **Tool Call Audits** | `10` |
| **Policy Blocks** | `1` |
| **Block Rate** | `10.0%` |

*Data regenerated and validated automatically: 2026-06-23T07:07:27.614701Z*

## Reproducibility Checklist

- [x] Multi-stage Docker packaging validation successful.
- [x] Cross-repository trace alignment schema compliance.
- [x] Telemetry export target verified.
