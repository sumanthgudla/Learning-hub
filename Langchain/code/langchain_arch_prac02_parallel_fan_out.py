from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnableParallel

llm=AzureChatOpenAI(
    api_version='2025-04-01-preview',
    azure_deployment='gpt-4.1',
    azure_endpoint='https://learning468.services.ai.azure.com/',
    api_key='REDACTED_AZURE_OPENAI_API_KEY'

)


summary_template=PromptTemplate.from_template("give me a summary on {topic}")
sentiment_template=PromptTemplate.from_template("Give me sentiment either positive negative or neutal on {topic}")
keywords_template=PromptTemplate.from_template("Give important keywords on {topic}")

topics=' 404 error means that the web server successfully connected but the specific page or file you requested could not be found. It is a standard HTTP status code indicating the content has been deleted, moved, or the web address was typed incorrectly.Common CausesIncorrect URL: A typo, misspelled word, or incorrect punctuation in the web address.Moved or Deleted Content: The page was taken down or permanently relocated to a new address without redirecting the old link.Broken Links: An external site or internal menu is pointing to an outdated address.How to Fix ItRefresh the page: Sometimes a temporary glitch prevents the page from loading properly.'

summary_chain= summary_template | llm
sentiment_chain= sentiment_template | llm
keyword_chain= keywords_template | llm

runnable_parallel=RunnableParallel(summary=summary_chain,sentiment=sentiment_chain,keyword=keyword_chain)
response=runnable_parallel.invoke({"topic":topics})

print(response)
