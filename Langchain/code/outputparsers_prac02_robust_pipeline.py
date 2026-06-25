from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Literal


llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    api_key='REDACTED_AZURE_OPENAI_API_KEY',
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/'
)

# 1. Define your updated schema
class CodeReview(BaseModel):
    language: str
    complexity: Literal["low", "medium", "high"]
    bugs: List[str]
    suggestions: List[str]
    refactored_snippet: str

prompt = ChatPromptTemplate([
    ('system', 'You are an experienced code analyst reviewing the code.'),
    ('user', 'Analyze the code below and respond ONLY with valid JSON.\n\n'
             'Code:\n{code}\n\n'
             '{format_instructions}')   # ← THIS was missing
])

parser=PydanticOutputParser(pydantic_object=CodeReview)

chain=prompt | llm | parser
response=chain.invoke({'code':'''
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
    print(message.content)''',
    'format_instructions': parser.get_format_instructions()  })

if response.complexity=='high':
    print("this code needs immediate intention")
print(response.complexity)