Here are the most important pieces you’ll use often:

Models (LLMs / Chat Models)
The “brain” that generates text.
Example: a chat model that answers questions.
Prompts (PromptTemplate / ChatPromptTemplate)
A reusable template for instructions.
Supports variables like {text}, {topic}, etc.
Output Parsers
Convert model output into the type you want:
plain string
JSON/dict
a validated structure
Chains / Runnables
The pipeline that connects prompt → model → parser.
Example: summarization chain.
Document Loaders + Text Splitters
Load text from PDFs/web/files and split into chunks.
Embeddings + Vector Stores + Retrievers
Used for RAG to store and fetch relevant chunks.
Agents + Tools
Used when the model needs to take actions (search, calculator, DB query).
Callbacks
Used for logging/debugging/monitoring timing and inputs/outputs.
