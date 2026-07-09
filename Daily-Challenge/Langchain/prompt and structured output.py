from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser


llm=AzureChatOpenAI(

)

prompt_template=ChatPromptTemplate(
    [
        ('system','you are an ai assistant'),
        ('user','answer the question {input}')
    ]
)

output_parser=StrOutputParser()
chain=prompt_template | llm | output_parser
print(chain.invoke({'input':'who is pm of india'}))