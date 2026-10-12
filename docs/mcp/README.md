# MCP for the FastAPI template

Developers can expose selected application services to MCP clients through the
same FastAPI process or a local stdio process. HTTP is disabled by default.

- [Quickstart](quickstart.md): connect a client over HTTP or stdio.
- [Architecture and research](architecture.md): SDK choice, protocol versions and ownership.
- [Add a capability](how-to.md): extend tools, resources or prompts with a concrete contract.
- [Reference and operations](reference.md): settings, authentication, deployment and troubleshooting.

The runnable [SDK client](../../examples/mcp_client.py) discovers capabilities,
calls `get_health_status` and reads `app://info`. Coding agents also read the
[MCP guidelines](../../.agents/mcp-guidelines.md) before changing this boundary.
