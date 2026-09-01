from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.chains


example_few_shot=[
    
    {
        "article": "The Federal Reserve raised benchmark interest rates by a quarter percentage point on Wednesday, fighting persistent inflation despite recent turmoil in the banking sector. Chairman Jerome Powell stated that borrowing costs might peak higher than previously expected if price pressures don't ease. The move brings the federal funds rate to a range of 4.75% to 5%. Stocks rallied briefly during the press conference but ended the day sharply lower.",
        "summary": "Overview: The Fed hiked interest rates by 0.25% to combat stubborn inflation amid banking sector stress.\n• Rates reached a new target range of 4.75% to 5%.\n• Powell hinted that peak rates could be higher than initially projected.\n• The stock market closed significantly down after a volatile afternoon."
    },
    {
        "article": "NASA's James Webb Space Telescope has captured a stunning new image of the heart of our galaxy, revealing unprecedented details about the dense environment surrounding the supermassive black hole Sagittarius A*. Utilizing its near-infrared camera, the telescope mapped over 500,000 stars in a region cosmic dust usually hides. Scientists say these findings will reshape theories on how stars form in extreme environments.",
        "summary": "Overview: The James Webb Space Telescope captured a highly detailed near-infrared image of the galactic center.\n• Over 500,000 stars were mapped through thick cosmic dust.\n• The imagery focuses heavily on the region around Sagittarius A*.\n• Data will help rewrite current theories on star formation."
    }

]

few_shot_messages=ChatPromptTemplate.from_messages(
    [
        ("user","{article}"),
        ("ai","{summary}")
    ]
)


Prompt_template=FewShotChatMessagePromptTemplate(
    example_prompt=few_shot_messages,
    examples=example_few_shot
    
)

chat_messages=ChatPromptTemplate.from_messages(
    [
        ("system","You are a summarizer"),
        Prompt_template,
        ("user","summarize this text {input}")
    ]
)

import os
from langchain_core.runnables import RunnableSequence
import json

llm=AzureChatOpenAI(
    azure_deployment="gpt-4.1",
<<<<<<< HEAD
    api_key=os.getenv("azure_api_key"),
=======
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
>>>>>>> 61b3936 (Changes)
    api_version="2025-04-01-preview",
    azure_endpoint="https://learning468.services.ai.azure.com/"
)

chain: RunnableSequence = chat_messages | llm

# Serialize runnable to dict and save to JSON (RunnableSequence has no .save())
chain_dict = chain.dict()
with open("prompt-chain.json","w",encoding="utf-8") as f:
    json.dump(chain_dict,f,ensure_ascii=False,indent=2)

print(chain.invoke({"input":"The Federal Reserve raised benchmark interest rates by a quarter percentage point on Wednesday, fighting persistent inflation despite recent turmoil in the banking sector. Chairman Jerome Powell stated that borrowing costs might peak higher than previously expected if price pressures don't ease. The move brings the federal funds rate to a range of 4.75% to 5%. Stocks rallied briefly during the press conference but ended the day sharply lower."}))

