How do you use LangChain to integrate with external APIs like OpenAI?
You use provider-specific wrappers, like ChatOpenAI.

import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "YOUR_KEY"

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)

response = llm.invoke("Explain RAG in 2 sentences.")
print(response.content)

Code explanation:

os.environ["OPENAI_API_KEY"] sets the API key for authentication.
ChatOpenAI(...) creates a model client configured with model name + temperature.
.invoke(...) sends a prompt to the model.
