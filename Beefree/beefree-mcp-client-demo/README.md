# Beefree MCP Client Demo

Minimal demo for editing a Beefree template through the Beefree SDK MCP v2 server instead of converting the template to simple JSON and asking an LLM to rewrite it.

## What this demonstrates

1. Creates an API-managed MCP template session from a Beefree template JSON.
2. Connects an MCP client to `https://api.getbee.io/v2/sdk/mcp`.
3. Lists Beefree MCP tools such as layout, content, style, and checker tools.
4. Optionally calls one MCP tool with JSON arguments.
5. Fetches the final template JSON after MCP changes.

## Setup

```bash
npm install
cp .env.example .env
```

Update `.env` with a Beefree **CSAPI key** from the SDK Console. Do not use `client_id` / `client_secret` in this demo and do not commit `.env`.

## Run

From this folder:

```bash
npm run demo -- --template ../sample-beefree.json --out output/final-template.json
```

List available MCP tools and their input schemas:

```bash
npm run list-tools -- --template ../sample-beefree.json
```

Call a specific MCP tool:

```bash
npm run call-tool -- --template ../sample-beefree.json --tool beefree_check_template --args '{}'
```

For editing tools, first run `--list-tools` and use the printed `inputSchema` to build the `--args` JSON.

## Target architecture

```text
Prompt / future LLM agent
        |
        v
Local MCP client
        |
        v
Beefree SDK MCP v2 endpoint
        |
        v
API-managed template session
```

This project is intentionally small. The next step is to wrap `listTools()` and `callTool()` with your Azure LLM/LangGraph agent so the model calls Beefree tools directly instead of generating modified template JSON.
