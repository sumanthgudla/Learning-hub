from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
import os
from dotenv import load_dotenv
import json

load_dotenv('.env')

api_key=os.getenv('azure_api_key')
llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key=api_key,
    api_version='2025-04-01-preview'
)

def get_weather(**kwargs):
    if kwargs['city'].lower() =='vizag':
        return '38 c'
    else:
        return '40 c'

def add_numbers(**kwargs):
    sum_nums=sum(kwargs.values())
    print(sum_nums)
    return sum_nums
print(get_weather(city='vizag'))  
print(add_numbers(a=5,b=10))    

system_instruction= """You are a AI Assistant with start, plan, action, observation and output state.
Wait for the user's prompt and plan first. 
After planning, take the action with appropriate input and wait for observation. 
After getting observation, return the AI response based on start prompt of the end prompt and observation.
Strictly follow the JSON output format as in examples.

Available Tools:
- function get_weather(city: string): string
This is a function that accepts a city name as string and returns the weather details.
-function add_numbers(list_nums)
This is a function that accepts multiple inputs a,b and returns the sum

Example:
START
{{ "type": "user", "user": "What is the sum of weather of Patiala and Mohali" }}
{{ "type": "plan", "plan": "I will call the get_weather_details for Patiala" }}
{{ "type": "action", "function": "get_weather_details", "input": {'city':'vizag'} }}
{{ "type": "observation", "observation": "10°C" }}
{{ "type": "plan", "plan": "I will call get_weather_details for Mohali" }}
{{ "type": "action", "function": "get_weather_details", "input": {'city':'Mohali'} }}
{{ "type": "observation", "observation": "14°C" }}
{{ "type": "plan", "plan": "Now I will sum the weather values of Vizag (38°C) and Mohali (40°C) using add_numbers function." }}
{{ "type": "action", "function": "add_numbers", "input": {'a':38,'b':40} }}
{{ "type": "output", "output": "The sum of weather of Patiala and Mohali is 24°C" }}"""
user_query = "What is sum of weather in vizag and goa"

messages = [
    SystemMessage(content=system_instruction),
    HumanMessage(
        content=json.dumps({"type": "user", "user": user_query}, ensure_ascii=False)
    ),
]

available_tools = {"get_weather": get_weather,'add_numbers':add_numbers}
count=0

while True:
    response=llm.invoke(messages)
    response_content=response.content
    try :
        json_data=json.loads(response_content)
    except :
        print('unable to parse the data')
    messages.append(AIMessage(content=response_content))   
    print(json_data)
    if json_data['type']=='plan':
        continue
    elif json_data['type']=='action':
        function_name=json_data['function']
        function_input=json_data['input']
        tool_result=str(available_tools[function_name](**function_input))
        messages.append(AIMessage(content=tool_result))
    elif json_data['type']=='output':
        break
