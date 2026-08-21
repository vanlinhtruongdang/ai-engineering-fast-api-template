# Agent Design Principles

Apply this guide only when a project created from the template adds AI agents, prompts, or multi-step agent workflows.

## Durable boundaries

- Define input, output, failure, and audit contracts before prompt wording.
- Keep validation and stable business rules in schemas or code, not only prompts.
- Store frequently changing rules in configuration or reference material.
- Extract instructions shared by more than one agent into reusable guidance.

## Agent contract

Each agent should state its role, mission, boundaries, input, output, decision rules, escalation rules, and expected audit evidence.

## Reliability

- Do not infer absent contract fields or invent workflow states.
- Keep orchestration instructions short and reusable fragments small.
- Retain trace references for nondeterministic output; logs do not replace validation.
- Recheck schemas, services, documentation, and tests together when an agent contract changes.
