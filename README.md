# Agentic Workflow Control Plane

A dependency-free proof of checkpointed agentic work: plan, execute, record an artifact, recover from failure, and stop for approval before an external action.

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
