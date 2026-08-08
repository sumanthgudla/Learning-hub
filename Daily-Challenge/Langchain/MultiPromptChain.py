from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain.globals import set_debug


set_debug(True)
class LearningNotes(BaseModel):
    topic:str
    summary:str
    keypoints:list[str]


load_dotenv('.env')

api_key=os.getenv('azure_api_key')
api_endpoint=os.getenv('azure_endpoint')


llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key=os.getenv("azure_api_key"),
    api_version='2025-04-01-preview'
)

detailed_summary_pompt=ChatPromptTemplate(
    [
        ('system','You are a content writer, your task is to write a summary on the given topic include only the facts '),
        ('user','Write detailed summary for the topic :{topic}')
    ]
)


structired_reponse_pronpt=ChatPromptTemplate(
    [
        ('system','you are a expert content summarizer. your task is to take the provided input and classify according to the provided output type'),
        ('user','your task is to structure the following input {message} into following {output}')
    ]
)

pydnacticoutput=PydanticOutputParser(pydantic_object=LearningNotes)
chain=detailed_summary_pompt | llm | RunnableLambda(lambda msg:{'message':msg.content,'output':pydnacticoutput.get_format_instructions()}) | structired_reponse_pronpt | llm | pydnacticoutput
result=chain.invoke({'topic':'Explain Python generators'})
print(result)