from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
KEY_VAULT_URL='https://key-vault-azure12.vault.azure.net/'
credential = DefaultAzureCredential()
secret_client = SecretClient(
    vault_url=KEY_VAULT_URL,
    credential=credential
)
def getllm():
    api_key = secret_client.get_secret(
        "my-ai-keyvault"
    ).value
    return AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key=api_key,
    api_version='2025-04-01-preview'
)