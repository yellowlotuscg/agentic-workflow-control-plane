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

## Implemented

The repository contains working code, not mockups:

- A `Job` record with a goal, an ordered list of steps, a state, an artifact store, and an event history (`workflow/engine.py`).
- A `WorkflowEngine` that executes each step against a small in-process action registry. The demo registers `research` and `draft` handlers that return synthetic content (`workflow/demo.py`).
- Checkpointed progress: each completed step stores its artifact and an event such as `completed:research`, so an interrupted job can be inspected step by step.
- A fail-closed approval gate: when a job reaches the `external_action` step, the engine stops immediately, sets state to `waiting_for_approval`, records an `approval_required` event, and returns without running anything beyond that point.
- Fail-closed handling of unknown steps: an unregistered step name marks the job `failed` with an `unknown_step:<name>` event instead of continuing or guessing.
- An append-only event history on each job (`started`, `completed:<step>`, `approval_required`, `failed`).

## Limitations

- The action registry is in-process only. Actions are plain Python callables; there is no live MCP server, tool discovery, namespace handling, or schema filtering in this proof of concept.
- Nothing is persisted. Jobs and events live only while the process runs.
- No external side effect is ever performed. The engine stops at `waiting_for_approval`; there is no sending, spending, or other outbound action.
- Retry, timeout, cancellation, and reconnect behavior are described as host responsibilities in the README but are not implemented in this code.
- Approval is a state transition only. There is no authentication, policy engine, or multi-operator review layer.
- All workflow content in the demo is synthetic.

## Tests

The standard-library `unittest` suite lives in `tests/test_engine.py` and verifies that a job running `research`, then `external_action`:

- records the `research` artifact before stopping;
- ends in state `waiting_for_approval`;
- records both `completed:research` and `approval_required` events.

Run it locally with `python -m unittest discover -s tests -v`. GitHub Actions runs the same command on every push to `main` and every pull request into `main` (see `.github/workflows/tests.yml`), with read-only token permissions and no credentials stored in the workflow.
