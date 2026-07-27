import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .config import get_llm
from .prompts import SYSTEM_INSTRUCTION
from .tools import run_tool


def run_react_agent(user_query: str):
    llm = get_llm()
    messages = [
        SystemMessage(content=SYSTEM_INSTRUCTION),
        HumanMessage(
            content=json.dumps({"type": "user", "user": user_query}, ensure_ascii=False)
        ),
    ]

    for _ in range(8):
        response = llm.invoke(messages)
        response_content = response.content

        try:
            json_data = json.loads(response_content)
        except json.JSONDecodeError:
            print('unable to parse the data')
            return {'status': 'error', 'message': response_content}

        messages.append(AIMessage(content=response_content))
        print(json_data)

        if json_data.get('type') == 'plan':
            continue

        if json_data.get('type') == 'action':
            function_name = json_data['function']
            function_input = json_data['input']
            tool_result = run_tool(function_name, function_input)
            messages.append(AIMessage(content=tool_result))
            continue

        if json_data.get('type') == 'output':
            return {'status': 'success', 'output': json_data.get('output')}

        return {'status': 'error', 'message': 'Unexpected response type', 'raw': json_data}

    return {'status': 'error', 'message': 'Maximum iterations reached'}
