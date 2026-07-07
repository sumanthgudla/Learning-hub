You typically install:
To install LangChain, we typically use pip. The basic installation command is:

PIP stands for "Pip Installs Packages".

It is Python's package manager, used to install, upgrade, and manage external Python libraries and dependencies from the Python Package Index (PyPI).

LangChain core package
Provider integration package (example: OpenAI)
pip install langchain
pip install langchain-openai


Why two installs?

langchain gives the framework components (prompts, chains, parsers, etc.)
langchain-openai gives the connector that knows how to call OpenAI models
