#Write a function to create a simple LangChain LLMChain for text summarization.
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
def TextSummarization(input):
    llm=AzureChatOpenAI(
        azure_deployment="gpt-4.1",
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2025-04-01-preview",
        azure_endpoint="https://learning468.services.ai.azure.com/"
    )
    chat_prompt=ChatPromptTemplate(
        [
            ('system','You are an expert in text summarization. sumamrize the provided text in bullet points'),
            ('user','{topic}')
        ]
    )
    chain=chat_prompt | llm
    print(chain.invoke({'topic':'runnable is written to prompt-chain.json. Want me to run the script now or update the serialization format (e.g., use LangChain\'s schema exporter) instead'}))




