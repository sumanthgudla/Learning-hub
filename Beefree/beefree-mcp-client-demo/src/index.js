import "dotenv/config";
import {
  createTemplateSession,
  fetchTemplate,
  readTemplate,
  withMcpClient,
  writeJson,
} from "./beefreeMcpClient.js";

const args = parseArgs(process.argv.slice(2));

const apiKey = process.env.BEEFREE_CSAPI_KEY;
if (!apiKey) {
  throw new Error("Missing BEEFREE_CSAPI_KEY. Copy .env.example to .env and add your Beefree CSAPI key.");
}

const templatePath = args.template ?? "../sample-beefree.json";
const outputPath = args.out ?? "output/final-template.json";
const apiBaseUrl = process.env.BEEFREE_API_BASE_URL;
const endpoint = process.env.BEEFREE_MCP_ENDPOINT;
const userHandle = process.env.BEEFREE_USER_HANDLE;

const template = await readTemplate(templatePath);
const templateId = await createTemplateSession({ apiKey, apiBaseUrl, template });
console.log(`Created Beefree MCP template session: ${templateId}`);

await withMcpClient({ apiKey, templateId, endpoint, userHandle }, async (client) => {
  const tools = await client.listTools();
  const toolList = tools.tools ?? [];
  console.log(`Connected to Beefree MCP. Available tools: ${toolList.length}`);

  if (args.listTools) {
    for (const tool of toolList) {
      console.log(`\n${tool.name}`);
      console.log(tool.description ?? "No description");
      console.log(JSON.stringify(tool.inputSchema, null, 2));
    }
    return;
  }

  if (args.tool) {
    const toolArgs = args.args ? JSON.parse(args.args) : {};
    const result = await client.callTool({
      name: args.tool,
      arguments: toolArgs,
    });
    console.log(`MCP tool result for ${args.tool}:`);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  const checkerTool = toolList.find((tool) => tool.name === "beefree_check_template");
  if (!checkerTool) {
    console.log("No tool requested. Use --list-tools to inspect available Beefree MCP tools.");
    return;
  }

  const result = await client.callTool({
    name: checkerTool.name,
    arguments: {},
  });
  console.log("Template check result:");
  console.log(JSON.stringify(result, null, 2));
});

const finalTemplate = await fetchTemplate({ apiKey, apiBaseUrl, templateId });
await writeJson(outputPath, finalTemplate);
console.log(`Wrote final template to ${outputPath}`);

function parseArgs(argv) {
  const parsed = {};

  for (let index = 0; index < argv.length; index += 1) {
    const current = argv[index];
    if (!current.startsWith("--")) {
      continue;
    }

    const key = current.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      parsed[toCamelCase(key)] = true;
      continue;
    }

    parsed[toCamelCase(key)] = next;
    index += 1;
  }

  return parsed;
}

function toCamelCase(value) {
  return value.replace(/-([a-z])/g, (_, char) => char.toUpperCase());
}
