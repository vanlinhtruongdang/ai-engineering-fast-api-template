# Agent design principles

Use this guide when a project built from the template adds an AI agent, prompt, tool, retrieval step, or multi-step workflow. This repository currently provides only empty `app/agents/` and `app/pipelines/` packages; no model provider, agent framework, queue, or persistence contract is preinstalled.

## Define the contract before prompts

For each concrete use case, record:

1. The caller and goal, accepted inputs, validation rules, and data classification.
2. The output schema, allowed states, and which component checks the result before it reaches an API caller or storage.
3. Tool permissions and trust boundaries: what the model may read, what it may change, and who authorizes external effects.
4. Failure behavior: timeout, provider failure, invalid output, retries, partial result, and the terminal response to the caller.
5. Audit evidence: request or run identifier, provider/model identifier when allowed, state transitions, and bounded error metadata. Keep secrets, raw private inputs, and sensitive model outputs out of routine logs.

For an agent, also name its role, decision authority, escalation condition, and the owner of final approval. A model-generated recommendation is not an authorization to call a mutating tool. Specify whether retries can repeat an external effect; use an idempotency or confirmation boundary when that effect must occur at most once.

Put stable validation and business rules in schemas and code. Prompt instructions can guide generation but cannot grant authorization, enforce a database invariant, or make untrusted tool output safe. Treat retrieved content and model output as untrusted until validated.

Define how the caller can distinguish success, refusal, invalid structured output, provider unavailability, and timeout. Do not silently coerce an absent field into a plausible answer or invent a workflow state to smooth over a partial result.

## Keep ownership explicit

- Put HTTP request/response behavior in `app/api/` and `app/schemas/`; use services for reusable business decisions. Add agent implementation under `app/agents/` only when a concrete consumer exists.
- Add orchestration under `app/pipelines/` only for a real multi-step process. Define durable state and recovery only if the workflow must survive interruption; do not imply durability from a Python function or in-memory task.
- Share a prompt fragment only after more than one current consumer needs the same invariant. Store changing domain reference material separately from hard validation rules.
- Select a provider, model, retrieval store, or agent framework from the use case's requirements. Do not add one to the template solely for discoverability.

## Verification and handoff

Check deterministic schema validation, permission decisions, and failure paths without depending on a live provider. Use recorded or controlled provider responses for local component tests. Run live calls only when explicitly authorized and report provider, cost-sensitive scope, and observed result without exposing private data.

When a contract changes, inspect callers, schemas, services, prompts, tool definitions, fixtures, documentation, and affected tests together. Report nondeterministic behavior as observed evidence with its limits; never request or expose private chain-of-thought.
