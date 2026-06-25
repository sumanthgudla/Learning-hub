from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI


llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key='REDACTED_AZURE_OPENAI_API_KEY'
)

llm1=AzureChatOpenAI(
    azure_deployment='gpt-4.2',
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key='REDACTED_AZURE_OPENAI_API_KEY'
)

reliable_model=llm1.with_fallbacks([llm])

max_tokens_model=reliable_model.bind(max_tokens=2)

chat_message=ChatPromptTemplate(
    [
        ('system','you ared an ai assistant'),
        ('user','hi')
    ]
)

chain=chat_message | max_tokens_model
for message in chain.stream({}):
    print(message.content)