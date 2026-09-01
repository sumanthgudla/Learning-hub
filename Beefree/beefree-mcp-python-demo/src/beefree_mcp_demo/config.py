from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


DEFAULT_API_BASE_URL = "https://api.getbee.io"
DEFAULT_MCP_ENDPOINT = "https://api.getbee.io/v2/sdk/mcp"


@dataclass(frozen=True)
class Settings:
    csapi_key: str
    api_base_url: str = DEFAULT_API_BASE_URL
    mcp_endpoint: str = DEFAULT_MCP_ENDPOINT
    user_handle: str | None = "demo-user"
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_deployment: str | None = None
    azure_openai_api_version: str = "2025-04-01-preview"


def load_settings() -> Settings:
    load_dotenv()

    csapi_key = getenv("BEEFREE_CSAPI_KEY")
    if not csapi_key:
        raise RuntimeError(
            "Missing BEEFREE_CSAPI_KEY. Copy .env.example to .env and add your Beefree CSAPI key."
        )

    return Settings(
        csapi_key=csapi_key,
        api_base_url=getenv("BEEFREE_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/"),
        mcp_endpoint=getenv("BEEFREE_MCP_ENDPOINT", DEFAULT_MCP_ENDPOINT),
        user_handle=getenv("BEEFREE_USER_HANDLE", "demo-user") or None,
        azure_openai_api_key=getenv("AZURE_OPENAI_API_KEY"),
        azure_openai_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_deployment=getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_openai_api_version=getenv(
            "AZURE_OPENAI_API_VERSION",
            "2025-04-01-preview",
        ),
    )


def require_azure_openai(settings: Settings) -> None:
    missing = [
        name
        for name, value in {
            "AZURE_OPENAI_API_KEY": settings.azure_openai_api_key,
            "AZURE_OPENAI_ENDPOINT": settings.azure_openai_endpoint,
            "AZURE_OPENAI_DEPLOYMENT": settings.azure_openai_deployment,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing Azure OpenAI settings for comment-based editing: "
            f"{', '.join(missing)}. Add them to .env or use list-tools/call-tool."
        )
