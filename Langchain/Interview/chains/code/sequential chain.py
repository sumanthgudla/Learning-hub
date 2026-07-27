from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnableLambda


llm=AzureChatOpenAI(
        azure_deployment="gpt-4.1",
        api_key=os.environ.get('AZURE_OPENAI_API_KEY'),
        api_version="2025-04-01-preview",
        azure_endpoint="https://learning468.openai.azure.com/",
        verbose=True
    )

prompt_message=ChatPromptTemplate(
    [
        SystemMessage('you are an ai assistant'),
        HumanMessage('generate joke on {topic}')
    ]
)

prompt_message2=ChatPromptTemplate(
    [
        SystemMessage('you are an ai assistant'),
        HumanMessage('generate summary  on {result}')
    ]
)
debug = RunnableLambda(
    lambda x: (print(type(x), x), x)[1]
)

chain = (
    prompt_message
    | llm
    | debug
    | RunnableLambda(lambda msg: {"result": msg.content})
    | debug
    | prompt_message2
    | llm
)

print(chain.invoke({'topic': 'india'}, config={"verbose": True}))
print(chain.get_graph().draw_ascii())
