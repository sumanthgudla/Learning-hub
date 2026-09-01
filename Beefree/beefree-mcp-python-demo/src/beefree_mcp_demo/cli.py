import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from beefree_mcp_demo.ai_editor import run_comment_edit
from beefree_mcp_demo.beefree_api import create_template_session, fetch_template
from beefree_mcp_demo.config import load_settings
from beefree_mcp_demo.job_runner import run_job_file
from beefree_mcp_demo.mcp_client import beefree_mcp_session


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        asyncio.run(run(args))
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


async def run(args: argparse.Namespace) -> None:
    settings = load_settings()

    if args.command == "run-job":
        await run_job_file(settings, args.job)
        return

    template = read_json(args.template)
    template_id = await create_template_session(settings, template)
    print(f"Created Beefree MCP template session: {template_id}")

    async with beefree_mcp_session(settings, template_id) as session:
        tools_result = await session.list_tools()
        tools = list(tools_result.tools)
        print(f"Connected to Beefree MCP. Available tools: {len(tools)}")

        if args.command == "list-tools":
            print_tools(tools)
        elif args.command == "call-tool":
            tool_args = json.loads(args.args)
            result = await session.call_tool(args.tool, tool_args)
            print_json_like(f"MCP tool result for {args.tool}", result)
        elif args.command == "edit":
            summary = await run_comment_edit(
                settings,
                session,
                args.instruction,
                max_steps=args.max_steps,
            )
            print(f"Edit summary:\n{summary}")
        else:
            checker = next(
                (tool for tool in tools if tool.name == "beefree_check_template"),
                None,
            )
            if checker is None:
                print("No default checker tool found. Use list-tools to inspect available tools.")
            else:
                result = await session.call_tool(checker.name, {})
                print_json_like("Template check result", result)

    final_template = await fetch_template(settings, template_id)
    write_json(args.out, final_template)
    print(f"Wrote final template to {args.out}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python Beefree SDK MCP v2 demo client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_common_args(subparsers.add_parser("demo", help="Run the basic MCP template check demo"))
    add_common_args(subparsers.add_parser("list-tools", help="List available Beefree MCP tools"))

    call_tool_parser = subparsers.add_parser("call-tool", help="Call one Beefree MCP tool")
    add_common_args(call_tool_parser)
    call_tool_parser.add_argument("--tool", required=True, help="MCP tool name")
    call_tool_parser.add_argument(
        "--args",
        default="{}",
        help="Tool arguments as a JSON object string",
    )

    edit_parser = subparsers.add_parser(
        "edit",
        help="Use Azure OpenAI to edit the template from a natural-language comment",
    )
    add_common_args(edit_parser)
    edit_parser.add_argument(
        "--instruction",
        required=True,
        help="Natural-language edit request, for example: generate a credit card email",
    )
    edit_parser.add_argument(
        "--max-steps",
        type=int,
        default=8,
        help="Maximum LLM/tool-call turns",
    )

    run_job_parser = subparsers.add_parser(
        "run-job",
        help="Run a backend-style JSON job file: input template + instruction -> output template",
    )
    run_job_parser.add_argument(
        "--job",
        required=True,
        help="Path to the job JSON file",
    )

    return parser


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--template",
        default="../sample-beefree.json",
        help="Path to the starting Beefree template JSON",
    )
    parser.add_argument(
        "--out",
        default="output/final-template.json",
        help="Path where the final template JSON should be written",
    )


def read_json(file_path: str) -> dict[str, Any]:
    with Path(file_path).open(encoding="utf-8") as file:
        value = json.load(file)

    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object in {file_path}")

    return value


def write_json(file_path: str, value: dict[str, Any]) -> None:
    output_path = Path(file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def print_tools(tools: list[Any]) -> None:
    for tool in tools:
        print(f"\n{tool.name}")
        print(getattr(tool, "description", None) or "No description")
        input_schema = getattr(tool, "inputSchema", None)
        print(json.dumps(to_jsonable(input_schema), indent=2))


def print_json_like(title: str, value: Any) -> None:
    print(f"{title}:")
    print(json.dumps(to_jsonable(value), indent=2))


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


if __name__ == "__main__":
    main()
