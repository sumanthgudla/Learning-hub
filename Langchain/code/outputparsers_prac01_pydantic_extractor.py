'''
Beginner — outputparsers_prac01_pydantic_extractor.py

Task: Define a Pydantic model MovieInfo with fields:

title: str

year: int

genre: str

rating: float

Build an LCEL chain that takes {"description": "..."} and extracts structured movie info using PydanticOutputParser. Test with:

"The Dark Knight is a 2008 crime thriller directed by Nolan, rated 9.0 on IMDb"

Expected:

pythonMovieInfo(title='The Dark Knight', year=2008, genre='crime thriller', rating=9.0)


'''
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class MovieInfo(BaseModel):
    title:str
    year:int



parser = PydanticOutputParser(pydantic_object=MovieInfo)
llm=AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    api_key='REDACTED_AZURE_OPENAI_API_KEY',
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/'
)

prompt = ChatPromptTemplate(
    [
        ('system', 'You are an assistant. extract the fields from the movie description'),
        ('user', 'The Dark Knight is a 2008 crime thriller directed by Nolan, rated 9.0 on IMDb')
    ]
)

chain=prompt | llm | parser
print(chain.invoke({}))

