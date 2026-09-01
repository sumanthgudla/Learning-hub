import json
from typing import Any

from mcp import ClientSession
from openai import AsyncAzureOpenAI

from beefree_mcp_demo.config import Settings, require_azure_openai


SYSTEM_PROMPT = """You edit Beefree email templates only by calling Beefree MCP tools.

Given the user's instruction, build or modify the template with available MCP tools.
For requests like "generate a credit card template", create a coherent email:
- subject/preheader if metadata tools are available
- hero section
- title and explanatory text
- benefits section
- call-to-action button
- visual styling such as background, text, and button colors

Do not invent tool names. Use only the provided tools and their schemas.
Prefer a small number of high-impact edits for this demo. After edits, call the
template checker tool if available, then finish with a concise summary."""


async def run_comment_edit(
    settings: Settings,
    session: ClientSession,
    instruction: str,
    max_steps: int = 8,
) -> str:
    require_azure_openai(settings)

    tools_result = await session.list_tools()
    mcp_tools = list(tools_result.tools)
    openai_tools = [to_openai_tool(tool) for tool in mcp_tools]

    client = AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=settings.azure_openai_api_version,
    )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": instruction},
    ]

    final_summary = "No final summary was returned by the model."
    for _ in range(max_steps):
        response = await client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto",
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            final_summary = message.content or final_summary
            break

        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments or "{}")
            result = await session.call_tool(tool_call.function.name, arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(to_jsonable(result)),
                }
            )

    return final_summary


def to_openai_tool(tool: Any) -> dict[str, Any]:
    input_schema = getattr(tool, "inputSchema", None) or {
        "type": "object",
        "properties": {},
    }
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": getattr(tool, "description", None) or "",
            "parameters": to_jsonable(input_schema),
        },
    }


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    return value
