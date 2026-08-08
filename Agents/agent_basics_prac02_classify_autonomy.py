from langchain_openai import AzureChatOpenAI
import os
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from dotenv import load_dotenv


load_dotenv('.env')
api_key=os.getenv('azure_api_key')
llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key=os.getenv("azure_api_key"),
    api_version='2025-04-01-preview'
)

Prompt=''' You are an ai assistant that helps classify the task into either three of tasks we have 
TASKS=[CHATBOT, WORKFLOW, AGENT]
Based on the user query choose either of them

STEPS TO CHOOSE:
1.Based on autonomy of the task choose one of them.
2.Go for agents only when it is must required
3.Go for WORKFLOW for email generation task
4. AGENT is used for coding purpose
5.CHATBOT is for general queries


ALWAYS CHOOSE ONLY ONE OF THEM
DO NOT PROVIDE ANY UNNECESSART TEXT
SOLE GOAL IS TO CHOOSE ONE OF THE TASK

EXAMPLES:
QUERY : WHAT IS AI
OUTPUT; CHATBOT


'''
query='wrote code on two sum'
prompts=[
    
        SystemMessage(content=Prompt),
        HumanMessage(content=query)
    
]

response=llm.invoke(prompts)
print(response.content)
