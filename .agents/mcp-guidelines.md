# MCP adapter guidelines

Read this guide for tools, resources, prompts, MCP transports, authorization
or client examples. The current contract is documented under
[`docs/mcp/`](../docs/mcp/README.md). `app/mcp/` uses the official `mcp` SDK v2;
do not substitute FastMCP APIs from a different package or SDK generation.

## Ownership and exposure

- MCP adapters call `app/services/` and share `app/schemas/` with REST. Business
  validation and each output contract have one owner. Do not call a REST
  endpoint through loopback HTTP when the service already owns the behavior.
- Register capabilities explicitly inside `create_server()`. Never expose all
  REST routes automatically or add a tool that calls arbitrary backend URLs.
- Each FastAPI factory owns its server; no mutable module singleton. The
  parent lifespan must enter and close `session_manager.run()` after creating
  the SDK HTTP app. Enabled MCP startup failure must fail app startup.
- Keep stdio independent of the HTTP application. Logging uses stderr/files;
  stdout is only protocol. HTTP remains opt-in at `/mcp/` on the same listener.

## Capability and trust contract

Before adding a capability, identify its caller, input/output schema, data
classification, errors and permission boundary. Use async handlers without
blocking work. Keep tool annotations accurate, but treat them as descriptions
rather than authorization enforcement.

For a tool that changes an external system, specify and enforce permission,
object access, idempotency and required human confirmation before the effect.
A model recommendation or a client's tool call is not sufficient authority.
Do not add retries without deciding whether they can duplicate effects.

Resource content, tool output and prompt inputs are untrusted data. Validate
identifiers and file/path inputs; prevent data content from being interpreted
as policy or permission. Never expose environment variables, secrets, raw
provider payloads or arbitrary filesystem contents as a resource.

## HTTP security and settings

`MCPSettings` validates enabled HTTP at app construction and masks its token.
Bearer middleware protects the mounted app before protocol dispatch. Retain
constant-time comparison, `401` plus `WWW-Authenticate: Bearer`, authentication
error signals, and secret-free logs. Keep SDK DNS-rebinding protection enabled;
configure explicit Host/Origin allowlists rather than a bypass switch.

CORS preflight belongs to existing FastAPI CORS middleware. Browser origins
must pass both CORS and MCP Origin policy. Remote deployments require HTTPS
and trusted proxy addresses for forwarded headers. Reviewed `.env.*` template
files with defaults and explicit placeholders may be versioned. Real tokens
belong in deployment secret injection or private `.env.*.local` overrides;
preserve existing developer files. Coordinate deployment values with DevOps.

The baseline shared token is only for team-controlled internal clients. It has
no user identity, per-client authorization or OAuth discovery. External client
access requires an explicit resource-server/IdP design with issuer,
audience/resource, expiry and scope validation using the SDK's auth APIs.

## Contract change checks

Inspect service and REST callers, registration/discovery, schemas,
authorization, client examples, tests and documentation together. A tool
failure (`is_error`) differs from a transport/protocol error. Clients must check
it before consuming `structured_content` and close transports with context
managers. Do not duplicate SDK JSON-RPC or request-limit implementations.

`tests/mcp/` belongs to the component lane. Keep settings environment/cache
isolation, HTTP tests with explicit parent lifespan, both protocol eras,
security/error paths and a real stdio subprocess check. New nontrivial behavior
needs focused proof; run `scripts/verify.sh` before handoff. Recheck the locked
SDK API when upgrading dependencies, including its use of `httpx2` for clients.
