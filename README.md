# Agentic Workflow Control Plane

A dependency-free proof of checkpointed agentic work: plan, execute, record an artifact, recover from failure, and stop for approval before an external action.

## MCP host pattern

An MCP **server** exposes capabilities. An MCP **host** owns the runtime that launches or connects to multiple servers, discovers their tools, namespaces collisions, applies an allowlist, and routes calls through policy.

A defensible host should provide:

- multiple stdio or HTTP connections with bounded timeouts;
- namespaced tool identifiers such as `mcp_git_search` and `mcp_docs_search`;
- an allowlist that exposes only the tools needed for the current workflow;
- schema filtering so unused tools do not consume the model context;
- cancellation, retry, and reconnect behavior;
- audit events recording server, tool, arguments class, result state, and approval state;
- explicit separation between read-only tools and side-effectful tools;
- fail-closed behavior when a server or policy decision is unavailable.

This repository demonstrates the host boundary without connecting to real accounts or external MCP servers. For the reference implementation and protocol details, see the [Model Context Protocol documentation](https://modelcontextprotocol.io/) and the [PixelRAG-style visual retrieval example](https://github.com/StarTrail-org/PixelRAG) for a separate multimodal use case.

## Philosophy

An agent is useful when its work is inspectable, interruptible, and recoverable. Planning is separate from execution. Tools are capabilities, not permissions. The final action remains a human decision.

## Run

```bash
python -m workflow.demo
python -m unittest discover -s tests -v
```

## Controls shown

- bounded steps and retries
- checkpointed state
- deterministic artifacts
- explicit approval gate
- fail-closed external action
- append-only event history

Synthetic lead data only. It does not contact customers or external services. Relevant practices include human-in-the-loop control, least privilege, idempotency, retry budgets, timeout boundaries, NIST AI RMF concepts, and OWASP LLM application-security guidance.
