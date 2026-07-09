"""Example tools for the demo agent.

These are intentionally tiny and synchronous so you can read how the agent
invokes them and how results are fed back to the LLM.
"""

from typing import Any


def python_eval(code: str) -> str:
    """Evaluate a simple Python expression and return the result as a string.

    WARNING: This uses a restricted eval for demo purposes. Do not use
    `eval` on untrusted inputs in production.
    """
    try:
        # very restricted globals and locals
        result = eval(code, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def reverse_text(text: str) -> str:
    """Simple utility tool: reverse the provided text."""
    return text[::-1]


def run_tool_by_name(name: str, inp: Any) -> str:
    """Dispatch helper used by the demo agent."""
    mapping = {
        "python_eval": python_eval,
        "reverse_text": reverse_text,
    }
    fn = mapping.get(name)
    if not fn:
        return f"Unknown tool: {name}"
    return fn(inp)
