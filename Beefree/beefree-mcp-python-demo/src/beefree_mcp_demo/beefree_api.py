from typing import Any

import httpx

from beefree_mcp_demo.config import Settings


async def create_template_session(
    settings: Settings,
    template: dict[str, Any],
    merge_tags: dict[str, Any] | None = None,
) -> str:
    payload: dict[str, Any] = {"template": template}
    if merge_tags is not None:
        payload["mergeTags"] = merge_tags

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{settings.api_base_url}/v2/sdk/mcp/template",
            headers={
                "Authorization": settings.csapi_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
        )

    body = parse_response_json(response)
    if response.is_error:
        raise RuntimeError(
            f"Failed to create Beefree MCP template session: "
            f"{response.status_code} {body}"
        )

    template_id = body.get("templateId") or body.get("id")
    if not template_id:
        raise RuntimeError(f"Beefree response did not include templateId: {body}")

    return str(template_id)


async def fetch_template(settings: Settings, template_id: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{settings.api_base_url}/v2/sdk/mcp/template/{template_id}",
            headers={
                "Authorization": settings.csapi_key,
                "Accept": "application/json",
            },
        )

    body = parse_response_json(response)
    if response.is_error:
        raise RuntimeError(
            f"Failed to fetch Beefree MCP template {template_id}: "
            f"{response.status_code} {body}"
        )

    template = body.get("template", body)
    if not isinstance(template, dict):
        raise RuntimeError(f"Expected final template object, received: {body}")

    return template


def parse_response_json(response: httpx.Response) -> dict[str, Any]:
    if not response.content:
        return {}

    try:
        body = response.json()
    except ValueError as error:
        raise RuntimeError(
            f"Expected JSON response but received: {response.text[:500]}"
        ) from error

    if not isinstance(body, dict):
        raise RuntimeError(f"Expected JSON object response, received: {body}")

    return body
