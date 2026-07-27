from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel

class SimpleWorkFlow(BaseModel):
    query:str
    

workflowGraph=StateGraph(SimpleWorkFlow)

def technical_answer(state:SimpleWorkFlow):
    print("Routed to technical")
    return {}

def general(state:SimpleWorkFlow):
    print("General answer")
    return {}

def ConditionalEdge(state: SimpleWorkFlow):
    input1=state.query
    allowed_keywords=["python", "llm", "langchain", "api"]
    if any(keyword in input1 for keyword in allowed_keywords):
        return "Technical"
    else:
        return "General"

workflowGraph.add_node('technical',technical_answer)
workflowGraph.add_node('general',general)

workflowGraph.add_conditional_edges(START,ConditionalEdge,{
    'Technical':'technical',
    'General':'general'
})
workflowGraph.add_edge('technical',END)
workflowGraph.add_edge('general',END)

app=workflowGraph.compile()
print(app.invoke({'query':'python is a simple language'}))

        