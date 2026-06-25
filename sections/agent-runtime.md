# Agent Runtime

## Overview

The `llm-agent-runtime` module implements the central execution layer for LLM-powered agents.
It provides a unified interface for tool registration, security-filtered dispatch, schema validation
of every tool call, and distributed span telemetry.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  AgentRuntime                   │
│                                                 │
│  register_tool(name, handler)                   │
│         │                                       │
│  execute(tool_name, arguments)                  │
│    ├── schema validation (tool_call.json)        │
│    ├── SecurityFilter(tool_name, args)           │
│    │      └── allowed? ─── NO ──► ToolCallBlocked│
│    ├── tool dispatch ──────────► handler()      │
│    └── span telemetry ─────────► _spans[]       │
│                                                 │
│  export_audit_report() ──────────► dict         │
└─────────────────────────────────────────────────┘
```

## Security Integration

Every tool call passes through a pluggable `security_filter` callable before dispatch.
The filter follows the interface:

```python
def filter(tool_name: str, arguments: dict) -> tuple[bool, str]:
    ...
```

This enables integration with `llm-security-governance` policies at runtime.

## Performance Metrics (Simulation)

| Metric               | Value             |
|----------------------|-------------------|
| Total calls          | 1,200             |
| Blocked calls        | 84 (7.0%)     |
| Allowed calls        | 1,116           |
| Tools registered     | 14              |
| Unique sessions      | 32              |
| p50 latency          | 1.2 ms           |
| p99 latency          | 8.7 ms           |

*Generated: 2026-06-22T20:11:56.398697Z*

## Span Telemetry

Each `execute()` call emits a span conformant to `llm-systems-core/schemas/span.json`:

```json
{
  "span_id": "<hex16>",
  "trace_id": "<hex32>",
  "name": "tool_call:<tool_name>",
  "service_name": "agent-runtime",
  "status": "ok | blocked | error",
  "attributes": {
    "call_id": "...",
    "tool_name": "...",
    "session_id": "..."
  }
}
```
