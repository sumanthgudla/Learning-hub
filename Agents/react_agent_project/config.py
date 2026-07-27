import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


load_dotenv('.env')


def get_llm() -> AzureChatOpenAI:
    api_key = os.getenv('azure_api_key')
    if not api_key:
        raise ValueError('azure_api_key is not set. Please add it to your .env file.')

    return AzureChatOpenAI(
        azure_deployment='gpt-4.1',
        azure_endpoint='https://learning468.services.ai.azure.com/',
        api_key=api_key,
        api_version='2025-04-01-preview',
    )
