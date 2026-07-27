# LangChain Agent Debug Demo

This small demo shows a minimal LangChain-style agent with explicit,
step-by-step logging so you can see LLM calls and tool invocations.

Quick start

1. Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r "langchain-agent-debug/requirements.txt"
```


2. Copy `.env.example` to `.env` and set credentials.

OpenAI (non-Azure) example:

```bash
OPENAI_API_KEY=sk-REPLACE_ME
```

Azure OpenAI example (set `USE_AZURE=true` or set `AZURE_OPENAI_API_BASE`):

```bash
AZURE_OPENAI_API_BASE=https://my-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=REPLACE_ME
AZURE_DEPLOYMENT_NAME=my-deployment
USE_AZURE=true
```

3. Run the agent:

```bash
python "langchain-agent-debug/run_agent.py"
```

Notes

- The demo intentionally keeps tool implementations tiny and synchronous.
- The agent expects the LLM to respond in a strict ACTION/INPUT or
  FINAL ANSWER format. This keeps parsing simple so you can inspect flows.
- The `python_eval` tool uses a restricted `eval` for demonstration only.
