from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_openai import AzureChatOpenAI
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
def get_conversion_rate(currency):
    if currency.lower()=='usd':
        return 90
    elif currency.lower()=='euro':
        return 110
    else:
        return 100

System_Prompt='''You are an AI Assistant with start plan observation and output state
Wait for user input and do the plan first
After planning take the appropriate action with appropriate input and wait for the obersvation
After getting the observation result either decide to do plan or prooduce the output result.
Always use the format provided in the examples.

Available Tools:


Examples
{{'type':'user','user':'how much is 100 USD in INR'}}
{{'type': 'plan','plan':'i will call the get_conversion_rate api for details with input of USD' }}
{{'type':'action','function':'get_conversion_rate','input':'USD'}}
{{'type':'observation','observation':'85'}}
{{'type':'output','output':'The value of 50 USD is 8000 INR}}

Always produce the result in json
'''

user_query='what is value of 100 USD and 50 EURO'

messages=[
    SystemMessage(content=System_Prompt),
    HumanMessage(content=json.dumps({'type':'user','user':user_query}))
]

available_tools={'get_conversion_rate':get_conversion_rate}
max_count=0
while True:
    max_count+=1
    if(max_count>10):
        break
    response=llm.invoke(messages).content
    messages.append(AIMessage(content=response))
    print(response)
    try:
        response_dict=json.loads(response)
    except:
        print('Not a json recieved ',response)
    if(response_dict['type']=='plan'):
        continue
    elif(response_dict['type']=='action'):
        function_name=response_dict['function']
        function_inputs=response_dict['input']
        tool_result=available_tools[function_name](function_inputs)
        observation=json.dumps({'type':'observation','observation':tool_result})
        messages.append(observation)
    elif(response_dict['type']=='output'):
        break
   
