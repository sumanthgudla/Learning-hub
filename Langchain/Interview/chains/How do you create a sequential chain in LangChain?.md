A sequential chain means: Step 1 output becomes Step 2 input, then Step 3, and so on.

Here’s an example: outline → expand into paragraph

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_sequential_chain():
    model = init_chat_model("openai:gpt-4.1-mini", temperature=0.2)
    parser = StrOutputParser()

    # Step 1: Create an outline
    outline_chain = (
        PromptTemplate.from_template("Create a 3-bullet outline on: {topic}")
        | model
        | parser
    )

    # Step 2: Expand the outline into a paragraph
    expand_chain = (
        PromptTemplate.from_template("Expand this outline into a short paragraph:\\n\\n{outline}")
        | model
        | parser
    )

    # Combine: output of outline_chain becomes input to expand_chain
    chain = outline_chain | (lambda outline: {"outline": outline}) | expand_chain
    return chain

Code explanation (simple):

outline_chain produces a string outline.
expand_chain expects an input variable called {outline}.
(lambda outline: {"outline": outline}) converts the string into the dict format the next prompt expects.
The | operator connects them in order.
Usage:

chain = create_sequential_chain()
print(chain.invoke({"topic": "RAG for beginners"}))

