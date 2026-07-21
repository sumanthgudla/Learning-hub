from langgraph.graph import StateGraph,START,END
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv('.env')

api_key=os.getenv('azure_api_key')
azure_endpoint=os.getenv('azure_endpoint')

llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint=azure_endpoint,
    api_version='2024-10-21',
    api_key=api_key
)


class SimpleGraph(BaseModel):
    input1:str
    response:str=''


stategraph=StateGraph(SimpleGraph)

def Error(State:SimpleGraph):
    print("Error no input provided")
    return {}

def GenerateAnswer(state:SimpleGraph):
    input1=state.input1
    response=llm.invoke(input1)
    return {'response':response.content}

def validate_input(state:SimpleGraph):
    input1=state.input1
    if input1 is None:
        return "Error"
    else :
        return "Generateanswer"


stategraph.add_node('Error_node',Error)
stategraph.add_node('Generate_answer_node',GenerateAnswer)
stategraph.add_conditional_edges(START,validate_input,{
    'Error':'Error_node',
    'Generateanswer':'Generate_answer_node'


}    
)
stategraph.add_edge('Error_node',END)
stategraph.add_edge('Generate_answer_node',END)

compiled_graph=stategraph.compile()
response=compiled_graph.invoke({'input1':'Write about AI'})
print(response)