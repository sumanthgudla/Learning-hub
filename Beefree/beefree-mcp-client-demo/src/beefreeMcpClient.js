import fs from "node:fs/promises";
import path from "node:path";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const DEFAULT_API_BASE_URL = "https://api.getbee.io";
const DEFAULT_MCP_ENDPOINT = "https://api.getbee.io/v2/sdk/mcp";

export async function readTemplate(templatePath) {
  const absolutePath = path.resolve(templatePath);
  const raw = await fs.readFile(absolutePath, "utf8");
  return JSON.parse(raw);
}

export async function writeJson(filePath, value) {
  const absolutePath = path.resolve(filePath);
  await fs.mkdir(path.dirname(absolutePath), { recursive: true });
  await fs.writeFile(absolutePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

export async function createTemplateSession({
  apiKey,
  apiBaseUrl = DEFAULT_API_BASE_URL,
  template,
  mergeTags,
}) {
  const response = await fetch(`${apiBaseUrl}/v2/sdk/mcp/template`, {
    method: "POST",
    headers: {
      Authorization: apiKey,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      template,
      ...(mergeTags ? { mergeTags } : {}),
    }),
  });

  const body = await parseJsonResponse(response);
  if (!response.ok) {
    throw new Error(`Failed to create Beefree MCP template session: ${response.status} ${JSON.stringify(body)}`);
  }

  const templateId = body.templateId ?? body.id;
  if (!templateId) {
    throw new Error(`Beefree template session response did not include templateId: ${JSON.stringify(body)}`);
  }

  return templateId;
}

export async function fetchTemplate({
  apiKey,
  apiBaseUrl = DEFAULT_API_BASE_URL,
  templateId,
}) {
  const response = await fetch(`${apiBaseUrl}/v2/sdk/mcp/template/${templateId}`, {
    headers: {
      Authorization: apiKey,
      Accept: "application/json",
    },
  });

  const body = await parseJsonResponse(response);
  if (!response.ok) {
    throw new Error(`Failed to fetch Beefree MCP template ${templateId}: ${response.status} ${JSON.stringify(body)}`);
  }

  return body.template ?? body;
}

export async function withMcpClient({
  apiKey,
  templateId,
  endpoint = DEFAULT_MCP_ENDPOINT,
  userHandle,
}, callback) {
  const client = new Client({
    name: "beefree-mcp-client-demo",
    version: "0.1.0",
  });

  const transport = new StreamableHTTPClientTransport(new URL(endpoint), {
    requestInit: {
      headers: {
        Authorization: apiKey,
        "x-bee-template-id": templateId,
        ...(userHandle ? { "x-bee-user-handle": userHandle } : {}),
      },
    },
  });

  await client.connect(transport);
  try {
    return await callback(client);
  } finally {
    await client.close();
  }
}

async function parseJsonResponse(response) {
  const text = await response.text();
  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`Expected JSON response but received: ${text.slice(0, 500)}`, { cause: error });
  }
}
