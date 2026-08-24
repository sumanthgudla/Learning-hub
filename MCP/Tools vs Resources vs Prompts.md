Topic 3 — Tools vs Resources vs Prompts. This is the one interviewers love to probe because it separates people who read the spec from people who just used a client.

## The three primitives

**Tools** — actions the LLM can *invoke*, with side effects. Think verbs: `send_email`, `update_block_text`, `create_issue`. The LLM decides to call them based on their name/description/schema, they take structured input, they return structured output (possibly after doing something in the real world). **Model-controlled** — the LLM chooses when to call a tool, based on the conversation.

**Resources** — read-only data the host can pull in as *context*, not something the LLM invokes mid-reasoning. Think nouns: a file's contents, a database schema, a Slack channel's history, a config file. They're identified by a URI (like `file:///path/to/thing` or `postgres://schema/table`). **Application-controlled** — typically the host/user decides to attach a resource to context (e.g. "attach this file"), not the LLM deciding mid-conversation.

**Prompts** — reusable, user-triggered templates the server exposes, often with slots to fill in. E.g. a "summarize-pr" prompt template a server provides so any client can offer it as a slash-command or menu action. **User-controlled** — surfaced as an explicit, invokable option in the UI, not something the LLM silently decides to use.

## The control-axis is the real distinction

This is the part worth memorizing because it's the actual design principle behind the split:

| Primitive | Who decides to use it | Analogy |
|---|---|---|
| Tool | The LLM (model-controlled) | Function call |
| Resource | The host/user (application-controlled) | Attaching a file |
| Prompt | The user (user-controlled) | Slash command / template |

Interviewers sometimes ask "why not just make everything a tool?" — the answer is that stuffing read-only context or canned templates into tool-calls wastes the LLM's decision-making on things that don't need a judgment call. Resources let you hand over data without spending an LLM turn deciding to fetch it; prompts let you standardize a common request without relying on the LLM to phrase the right instructions itself.

## Map this onto Beefree

Beefree's MCP server exposing "update block text," "delete block," "add image block" — those are **tools**, because the LLM decides which editing operation to perform based on the user's request. If Beefree's server also exposed something like "current template schema" as a **resource**, that'd be read-only context the host could load in, not something the LLM invokes as an action.

## Say it out loud

*"Tools are invokable actions the model chooses to call — like updating a block. Resources are read-only context the application attaches, like a file or schema. Prompts are reusable templates the user explicitly triggers. The real distinction is who's in control: model, application, or user."*

Ready for topic 4 — the request/response lifecycle (initialize → list tools → call tool → result)?