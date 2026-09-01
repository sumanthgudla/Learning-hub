# Beefree MCP Python Demo

Python-only demo for editing Beefree templates through the Beefree SDK MCP v2 server.

This replaces the old flow where a template is converted to simple JSON and the LLM rewrites the whole JSON. With MCP, your agent can call Beefree tools directly, for example to add rows, add columns, add text, update colors, validate the template, and then fetch the final template JSON.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Beefree **CSAPI key** to `.env`:

```text
BEEFREE_CSAPI_KEY=your_csapi_key_here
```

For natural-language editing, also add Azure OpenAI values:

```text
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

Do not put Beefree credentials in source code.

## Commands

Run from this folder.

List available Beefree MCP tools:

```bash
PYTHONPATH=src python -m beefree_mcp_demo.cli list-tools --template ../sample-beefree.json
```

Call a tool directly:

```bash
PYTHONPATH=src python -m beefree_mcp_demo.cli call-tool --template ../sample-beefree.json --tool beefree_check_template --args '{}'
```

Run the simple demo, which creates an MCP session, checks the template when the checker tool is available, and writes the final JSON:

```bash
PYTHONPATH=src python -m beefree_mcp_demo.cli demo --template ../sample-beefree.json --out output/final-template.json
```

Edit from a natural-language comment using CLI args:

```bash
PYTHONPATH=src python -m beefree_mcp_demo.cli edit \
  --template ../sample-beefree.json \
  --instruction "Generate a credit card offer email. Add a hero row, two columns, benefits text, a CTA button, and use blue and gold colors." \
  --out output/credit-card-template.json
```

## Backend-style file input/output

Use `run-job` when you want to provide an input JSON file, call the agent with Beefree MCP tools, and produce the edited template JSON in an output file.

Sample job file:

```json
{
  "template_path": "../sample-beefree.json",
  "instruction": "Generate a credit card offer email. Add a hero row, two columns, benefits text, a CTA button, and use blue and gold colors.",
  "output_path": "output/credit-card-template.json",
  "max_steps": 8,
  "merge_tags": {
    "first_name": "Sumanth"
  }
}
```

Run it:

```bash
PYTHONPATH=src python -m beefree_mcp_demo.cli run-job --job sample-job.json
```

The job file supports either:

- `template_path`: path to a Beefree template JSON file, resolved relative to the job file
- `template`: inline Beefree template JSON object

Required fields:

- `instruction`: your natural-language editing comment
- `output_path`: where to save the final Beefree template JSON

## How comment-based editing works

The `edit` command takes a user comment such as:

```text
Generate a credit card offer email. Add a hero row, two columns, a benefits section, a CTA button, and use blue/gold colors.
```

Then the agent should:

1. Create a Beefree MCP template session.
2. List available MCP tools and schemas.
3. Provide those tools to Azure OpenAI as callable functions.
4. Call Beefree MCP tools such as add section, add title, add paragraph, add button, and update style.
5. Run `beefree_check_template`.
6. Fetch the final template JSON.

FastAPI is intentionally skipped for now because the first goal is API learning from Python. Add FastAPI later only if a browser or another service needs HTTP endpoints.
