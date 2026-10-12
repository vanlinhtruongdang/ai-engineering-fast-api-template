# Add an MCP capability

Use this guide when a specific client needs a tool, resource or prompt. Start
from [the server factory](../../app/mcp/server.py) and read
[the agent rules](../../.agents/mcp-guidelines.md). Registration is explicit;
adding a REST route does not automatically expose it over MCP.

## Define the contract and owner

1. Name the caller, accepted inputs, output schema and data it may access.
   Choose a tool for an operation, a resource for addressable content, or a
   prompt for a reusable message template. Do not add all three for one use case.
2. Put business validation in `app/services/` and its shared contract in
   `app/schemas/`. The MCP adapter handles protocol representation; REST keeps
   HTTP status/response handling. Inspect every existing caller before changing
   a shared schema or service.
3. Define errors and permissions. A tool's `is_error=true` is distinct from an
   HTTP/transport failure or a JSON-RPC protocol error. Return actionable,
   bounded errors without raw inputs, credentials or upstream responses.
4. For an external effect, define who authorizes it, which scope/object is
   allowed, how duplicate calls behave, and which confirmation is required.
   Apply checks before the service changes anything. Read-only annotations do
   not replace those checks.

## Register the adapter

The existing health tool is the smallest working pattern: an async handler
calls a service and returns `HealthResponse`. Type hints generate input and
output schemas; a Pydantic result produces `structured_content`. Keep
annotations accurate (`read_only_hint`, `destructive_hint`, `idempotent_hint`,
`open_world_hint`). Do not wrap every REST endpoint or accept arbitrary URLs
for calling another backend.

For a JSON resource, follow `app://info`: register a URI and
`mime_type="application/json"`, then serialize the service's Pydantic result
with `model_dump_json()`. For parameterized resources, validate identifiers,
object access and any path inputs before reading data. The SDK's resource
security is an additional boundary rather than domain authorization.

Register a prompt only when a caller needs a reusable message contract. This
baseline exposes no prompts. This is an illustrative SDK registration for a
project that needs to explain a validated status:

```python
from typing import Literal

@server.prompt()
async def explain_health(status: Literal["ok", "unavailable"]) -> str:
    """Ask the host to explain a validated health status."""
    return f"Explain the application health status: {status}."
```

Place registrations inside `create_server()`, so both transports expose the
same contract. A prompt returns messages for a host; it does not run a model.
Treat prompt input, retrieved resources and tool output as untrusted content.
Never let instructions inside that content grant permission or replace
system policy. See the SDK's
[tools](https://py.sdk.modelcontextprotocol.io/servers/tools/),
[resources](https://py.sdk.modelcontextprotocol.io/servers/resources/) and
[prompts](https://py.sdk.modelcontextprotocol.io/servers/prompts/) guides.

## Verify and document the change

Add a focused check under `tests/mcp/` for discovery names, input/output
schemas, valid calls, rejected inputs and permission/error paths. Exercise
both `Client(..., mode="auto")` and `mode="legacy"` when the behavior must work
in both protocol eras. Verify HTTP auth and shared REST callers still hold.
For resources/prompts, verify the URI or arguments, MIME/message type and
untrusted-content handling rather than snapshotting prose.

```bash
scripts/test-suite.sh component tests/mcp
scripts/verify.sh
```

Update the [capability reference](reference.md), affected client examples and
service/REST tests in the same change. If the use case requires subscriptions,
durability or server-initiated callbacks, revisit the current stateless
transport contract explicitly instead of hiding state in a module singleton.
