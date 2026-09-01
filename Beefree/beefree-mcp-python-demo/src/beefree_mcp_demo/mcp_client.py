from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.shared._httpx_utils import create_mcp_http_client

from beefree_mcp_demo.config import Settings


@asynccontextmanager
async def beefree_mcp_session(
    settings: Settings,
    template_id: str,
) -> AsyncIterator[ClientSession]:
    headers = {
        "Authorization": settings.csapi_key,
        "x-bee-template-id": template_id,
    }
    if settings.user_handle:
        headers["x-bee-user-handle"] = settings.user_handle

    async with create_mcp_http_client(headers=headers) as http_client:
        async with streamable_http_client(settings.mcp_endpoint, http_client=http_client) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session


async def list_tools(settings: Settings, template_id: str) -> list[Any]:
    async with beefree_mcp_session(settings, template_id) as session:
        result = await session.list_tools()
        return list(result.tools)


async def call_tool(
    settings: Settings,
    template_id: str,
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    async with beefree_mcp_session(settings, template_id) as session:
        return await session.call_tool(tool_name, arguments)
