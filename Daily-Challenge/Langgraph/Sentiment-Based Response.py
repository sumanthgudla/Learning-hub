from langgraph.graph import StateGraph,START,END
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal


load_dotenv('.env')

api_key=os.getenv('azure_api_key')
azure_endpoint=os.getenv('azure_endpoint')

llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    azure_endpoint=azure_endpoint,
    api_version='2024-10-21',
    api_key=api_key
)

class SentimentAnalysis(BaseModel):
    input_text: str
    sentiment:Literal['positive','negative']=''

sentimentgraph=StateGraph(SentimentAnalysis)

sentiment_analysis_pronpt=ChatPromptTemplate(
    [
        ('system','You are sentiment analyzer. your task is to analyze the sentiment for a given phrase either as positive or negative'),
        ('user','Analyze the sentiment for the topic : {topic}' )
    ]
)


def AnalysisSentence(state:SentimentAnalysis):
    input_text=state.input_text
    chain=sentiment_analysis_pronpt | llm
    result=chain.invoke({'topic': input_text})
    return {'sentiment': result.content.lower()}

def routingSentence(state:SentimentAnalysis):
    sentiment=state.sentiment.lower()
    if sentiment == 'positive':
        return 'ThankUser'
    else:
        return 'Escalate'


def Thankuser(state:SentimentAnalysis):
    print('Thanks user')
    return {}

def Escalate(state:SentimentAnalysis):
    print("Escalating to higher team")
    return {}



sentimentgraph.add_node('AnalysisSentence',AnalysisSentence)
sentimentgraph.add_node('Thankuser',Thankuser)
sentimentgraph.add_node('Escalate',Escalate)

sentimentgraph.add_edge(START,'AnalysisSentence')
sentimentgraph.add_conditional_edges('AnalysisSentence',routingSentence,
    {
        'ThankUser':'Thankuser',
        'Escalate':'Escalate'
    }
)

sentimentgraph.add_edge('Thankuser',END)
sentimentgraph.add_edge('Escalate',END)

compiled_graph=sentimentgraph.compile()
result=compiled_graph.invoke({'input_text':'This product is good'})
print(result)

