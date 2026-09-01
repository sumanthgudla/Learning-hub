import json
from pathlib import Path
from typing import Any

from beefree_mcp_demo.ai_editor import run_comment_edit
from beefree_mcp_demo.beefree_api import create_template_session, fetch_template
from beefree_mcp_demo.config import Settings
from beefree_mcp_demo.mcp_client import beefree_mcp_session


async def run_job_file(settings: Settings, job_path: str) -> dict[str, Any]:
    job = read_json_object(job_path)
    instruction = require_string(job, "instruction")
    output_path = require_string(job, "output_path")
    max_steps = int(job.get("max_steps", 8))
    merge_tags = job.get("merge_tags")

    if "template" in job:
        template = job["template"]
        if not isinstance(template, dict):
            raise RuntimeError("job.template must be a JSON object when provided.")
    elif "template_path" in job:
        template = read_json_object(str(resolve_from_job(job_path, require_string(job, "template_path"))))
    else:
        raise RuntimeError("Job must include either template_path or template.")

    if merge_tags is not None and not isinstance(merge_tags, dict):
        raise RuntimeError("job.merge_tags must be a JSON object when provided.")

    template_id = await create_template_session(
        settings,
        template=template,
        merge_tags=merge_tags,
    )
    print(f"Created Beefree MCP template session: {template_id}")

    async with beefree_mcp_session(settings, template_id) as session:
        summary = await run_comment_edit(
            settings,
            session,
            instruction,
            max_steps=max_steps,
        )

    final_template = await fetch_template(settings, template_id)
    resolved_output_path = resolve_from_job(job_path, output_path)
    write_json(resolved_output_path, final_template)

    result = {
        "template_id": template_id,
        "instruction": instruction,
        "summary": summary,
        "output_path": str(resolved_output_path),
    }
    print(json.dumps(result, indent=2))
    return result


def read_json_object(file_path: str) -> dict[str, Any]:
    with Path(file_path).open(encoding="utf-8") as file:
        value = json.load(file)

    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object in {file_path}")

    return value


def write_json(file_path: Path, value: dict[str, Any]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def require_string(value: dict[str, Any], key: str) -> str:
    field = value.get(key)
    if not isinstance(field, str) or not field.strip():
        raise RuntimeError(f"Job must include a non-empty string field: {key}")
    return field


def resolve_from_job(job_path: str, target_path: str) -> Path:
    path = Path(target_path)
    if path.is_absolute():
        return path
    return Path(job_path).resolve().parent / path
