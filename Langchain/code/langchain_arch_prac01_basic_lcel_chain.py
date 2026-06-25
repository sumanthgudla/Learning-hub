# simple_azure_chat.py
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

# Initialize Azure ChatOpenAI
llm = AzureChatOpenAI(
    azure_endpoint="https://learning468.services.ai.azure.com/",
    azure_deployment="gpt-4.1",   # e.g., "gpt-4o"
    api_version="2025-04-01-preview",
    api_key="REDACTED_AZURE_OPENAI_API_KEY",
    temperature=0.7,
)


prompt_template=PromptTemplate.from_template("give a detailed overview on {country}")

prompt_message=prompt_template.format(country="india") 
# Simple chat with messages

string_output=StrOutputParser()
chain = prompt_template | llm | string_output

for message in chain.stream({"country":"india"}):
    print(message,end="")

