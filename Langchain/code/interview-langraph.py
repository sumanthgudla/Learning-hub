from langgraph.graph import StateGraph,START,END
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

llm = AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    model='gpt-4',
<<<<<<< HEAD
    api_key=os.getenv("azure_api_key"), # Note: Keep keys secure in production!
=======
    api_key='REDACTED_AZURE_OPENAI_API_KEY', # Note: Keep keys secure in production!
>>>>>>> 61b3936 (Changes)
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/'
)

class ResponseState(BaseModel):
    input:str
    output:str


def LLM_Response(state:ResponseState ):
    input=state.input
    prompt_message=ChatPromptTemplate(
        [
        ('system','you are an ai assitant'),
        ('user','''hi from langchain_openai import AzureChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import PydanticOutputParser
    from pydantic import BaseModel''')
        ]
    )
    chain = prompt_message | llm 
    response=chain.invoke({})
    return {'output':response.content}


graph=StateGraph(ResponseState)
graph.add_node('llmresponse',LLM_Response)
graph.add_edge(START,'llmresponse')
graph.add_edge('llmresponse',END)
compiled_graph=graph.compile()
response=compiled_graph.invoke({"input": "What is LangGraph?"})
print(response)
