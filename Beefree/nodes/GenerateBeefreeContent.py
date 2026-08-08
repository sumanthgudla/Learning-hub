import json
from azurellm import getllm
from state import BeefreeState
def GenerateBeefreeContent(state:BeefreeState):
    llm=getllm()
    input_json=json.dumps(state.simple_schema)
    response=llm.invoke(state.messages).content
    json_response=json.loads(response)
    return {'ai_schema':json_response} 