from langgraph.graph import StateGraph,START,END
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
import json
from langchain_core.messages import SystemMessage,HumanMessage
from azurellm import getllm
from nodes.GenerateBeefreeContent import GenerateBeefreeContent
from state import BeefreeState
from nodes.convert_simple_schema import convertsimpleschema
from nodes.validate_schema import validate
from prompts.beefree_prompt import USER_PROMPT,SYSTEM_PROMPT

llm=getllm()
beefreegraph=StateGraph(BeefreeState)

beefreegraph.add_node('GenerateBeefreeContent',GenerateBeefreeContent)
beefreegraph.add_node('simple_schema',convertsimpleschema)
beefreegraph.add_node('validate_schema',validate)


beefreegraph.add_edge(START,'simple_schema')
beefreegraph.add_edge('simple_schema','GenerateBeefreeContent')
beefreegraph.add_edge('GenerateBeefreeContent','validate_schema')
beefreegraph.add_edge('GenerateBeefreeContent',END)

messages=[
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=USER_PROMPT.format(
        user_input="Generate a sales email on the provided JSON. Only update the JSON.",
    ))
]

compiled_beefree_graph=beefreegraph.compile()
with open ('sample-beefree.json','r') as f:
    content=json.load(f) 
print(content)
response=compiled_beefree_graph.invoke({'messages':messages,'original_schema':content})
json_response=json.dumps(response["ai_schema"])
print(json_response)

with open('output-beefree.json','w') as fout:
    fout.write(json_response)



