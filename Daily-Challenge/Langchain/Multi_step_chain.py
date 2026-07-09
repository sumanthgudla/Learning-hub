from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv('.env')

api_key=os.getenv('azure_api_key')
api_endpoint=os.getenv('azure_endpoint')

print(api_key)

class summary(BaseModel):
    title:str
    summary:str
    difficulty:str

llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    api_version='2024-10-21',
    api_key=api_key,
    azure_endpoint=api_endpoint
)

conscise_prompt=ChatPromptTemplate(
    [
        ('system','You are an ai assistant to write concise information on the given topic'),
        ('user','The topic is on {topic}')
    ]
)

output=PydanticOutputParser(pydantic_object=summary)

json_summary_prompt=ChatPromptTemplate(
    [
        ('system','you are an expert in summarizing a brief topic into dividing into specific catgories as per the required output state'),

        ('user','analyze the topic and divide into specific categories for the {request} in the format of {format_instructions}')
    ]

)



chain= json_summary_prompt | llm | output
print(chain.invoke({'request':'This standard LCEL sequence formats your prompt, sends it to the language model, and parses the text into a structured JSON output.','format_instructions':output.get_format_instructions()}))