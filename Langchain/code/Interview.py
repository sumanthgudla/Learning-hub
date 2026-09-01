from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
<<<<<<< HEAD
    api_key=os.getenv("azure_api_key"),
=======
    api_key='REDACTED_AZURE_OPENAI_API_KEY',
>>>>>>> 61b3936 (Changes)
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/'
)

class Summary(BaseModel):
    summary:str
prompt_message=ChatPromptTemplate(
    [
    ('system','you are an ai assitant'),
    ('user','''hi from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel''')
    ]
)
pydantic_output=PydanticOutputParser(pydantic_object=Summary)
chain = prompt_message | llm | pydantic_output
response=chain.invoke({})
print(response)