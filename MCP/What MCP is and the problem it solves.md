Let's lock in topic 1 — say it out loud as you read, like you're already answering the interviewer.

## What MCP Is (in one line)

**MCP (Model Context Protocol) is a standard way for an LLM application to discover and call external tools, without every app needing a custom integration for every tool.**

## The problem it solves

Before MCP, if you wanted an LLM to control, say, Slack, GitHub, and a database, you had three options, all bad at scale:

- **Hand-roll function-calling schemas** for each tool, for each app, individually. Every team that wants to connect Claude/GPT to GitHub writes their own GitHub integration. If 50 apps want GitHub access, that's 50 redundant integrations.
- **N×M integration explosion**: N applications (Claude Desktop, your IDE, a chatbot) × M tools (GitHub, Slack, a database) = N×M custom glue code paths. Nobody wants to write that many integrations.
- **No standard contract** for how tool descriptions, inputs, outputs, or errors should look, so nothing is reusable or portable across LLM apps.

MCP fixes this the way USB-C fixed device charging, or the way LSP (Language Server Protocol) fixed "every IDE needs its own integration with every programming language." One protocol, and:

- **Tool authors** (e.g. Beefree, GitHub, a database vendor) build **one MCP server** exposing their capabilities.
- **Any MCP-compatible client** (Claude Desktop, an IDE, your own agent) can talk to that server without custom code.
- It collapses N×M integrations down to **N+M**: each app implements MCP once (client side), each tool implements MCP once (server side), and now they all interoperate.

## Say this out loud as your one-breath answer

*"MCP standardizes how LLM applications discover and call external tools — instead of every app writing custom integration code for every tool, both sides just implement one protocol, and any compliant client can use any compliant server."*

That's the elevator pitch. Once that's solid, we move to topic 2 — host/client/server roles, which is where people's answers usually get muddy in interviews (they conflate "client" and "host"). Ready to move on, or want to drill this one more before advancing?