from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv('.env')
azure_key=os.getenv('azure_api_key')
llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    api_key=azure_key,
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/'
)
response=llm.invoke('what is paris')
print(response)