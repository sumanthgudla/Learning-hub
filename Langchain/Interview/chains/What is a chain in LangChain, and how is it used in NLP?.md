What is a chain in LangChain, and how is it used in NLP?
Fullscreen
A chain in LangChain is a workflow (pipeline) that connects multiple steps to solve an NLP task end-to-end.

A chain typically includes:

Prompt (what you ask the model + placeholders)
Model (LLM/chat model that generates text)
Parser (converts raw output into a clean format like string/JSON)
Optional extras: retriever, tools, memory, validators
How chains help in NLP:

Summarization: text → prompt → model → summary
Question answering: context + question → prompt → model → answer
RAG: question → retrieve docs → prompt with docs → model → grounded answer
Extraction: messy text → prompt → model → structured JSON
Beginner-friendly analogy:

A chain is like a cooking recipe:

gather ingredients (inputs)
follow steps (prompt + model calls)
plate the dish nicely (parser/formatting)
