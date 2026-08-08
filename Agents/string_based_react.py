from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv('.env')
api_key=os.getenv('api_key')
llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key=os.getenv("azure_api_key"),
    api_version='2025-04-01-preview'
)

System_prompt='''
You are an AI assistant with plan action and action approach method. Always go step by step , user->plan->action 
Wait for the user's prompt and plan first. do not generate action during the plan , go step by step
After planning, take the action with appropriate input and wait for observation. 
After getting observation, return the AI response based on start prompt of the end prompt and observation.


TOOLS AVALABLE:
[calculator, search]
search takes a input string and produes a output
calcualtor takes a expression , evaluates and produces output
example '2+3' produces 5 , always provide input in string

Examples:
user : give me population of france by 2
plan: i need to find the find the popuklation of france first:
action : search['population of france']
observation: the population of france is 50000
plan: now i need to divide the poulation by 2
action : calcualor[50000,divide,2]
observation  25000
output: the final result is 25000

GUARDRAILS
Do not produce any extra output apart from the pattern
Produce one result at a time to achive the goal
Do not generate action during the plan itself , go step by step Wait for the next message before continuing..

'''
query=' what is number of bricks in india by 2'
messages=[
    SystemMessage(content=System_prompt),
    HumanMessage(content='user :'+query)
]

def search(query):
    if 'India' in query:
        return 50000000
    else:
        return 10000000
def calculator(expression):
    return eval(expression)


functions={'search':search, "calculator": calculator}

while(True):
    response=llm.invoke(messages).content
    llm_action=response.split(':')[0]
    llm_output=response.split(':')[1]
    print(llm_action)
    print(llm_output)
    messages.append(AIMessage(content=response))
    if llm_action.lower()=='plan':
        continue
    if llm_action.lower()=='action':
        function=llm_output.split('[')[0].strip()
        parameter=llm_output.split('[')[1].split(']')[0].strip()
        print(function)
        print(parameter)
        tool_result=functions[function](parameter)
        observation_result='observation : ' +str(tool_result)
        print(observation_result)
        messages.append(HumanMessage(content=observation_result))
    if llm_action.lower()=='output':
        print(llm_output)
        break
