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
| Rag | 1.002 ms |
| Security | 0.000 ms |
| Agent-runtime | 1.000 ms |

### Security Auditing Summary

| Telemetry Dimension | Capture Metric |
| :--- | :--- |
| **Trace ID** | `446377bdc65d4172b2e96b2a78dceca0` |
| **Total Captured Spans** | `15` |
| **Tool Call Audits** | `4` |
| **Policy Blocks** | `1` |
| **Block Rate** | `25.0%` |

*Data regenerated and validated automatically: 2026-06-23T06:57:54.081486Z*

## Reproducibility Checklist

- [x] Multi-stage Docker packaging validation successful.
- [x] Cross-repository trace alignment schema compliance.
- [x] Telemetry export target verified.
