from pydantic import BaseModel
from typing import TypedDict, Annotated,Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class BeefreeState(BaseModel):
    original_schema:dict[str,Any]=''
    messages:Annotated[list[BaseMessage], add_messages]
    simple_schema:dict[str,Any]=''
    ai_schema:dict[str,Any]=''
    is_validated:bool=False