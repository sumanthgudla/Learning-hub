from langchain_openai import AzureChatOpenAI
def getllm():
    return AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key=os.getenv("azure_api_key"),
    api_version='2025-04-01-preview'
)