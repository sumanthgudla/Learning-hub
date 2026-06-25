from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize LLM
llm = AzureChatOpenAI(
    azure_deployment='gpt-4.1',
    model='gpt-4',
    api_key='REDACTED_AZURE_OPENAI_API_KEY', # Note: Keep keys secure in production!
    api_version='2025-04-01-preview',
    azure_endpoint='https://learning468.services.ai.azure.com/'
)

# 2. Initialize memory with max_token_limit=150 (as per task instructions)
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=150,  # Lowered to match task constraint and trigger summarization faster
    return_messages=True,
    memory_key='history',
)

# 3. Define the Prompt with MessagesPlaceholder matching the memory_key
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful AI assistant.'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{input}')  # Made dynamic instead of static 'hi'
])

# 4. Build the LCEL Chain
# We use RunnablePassthrough to feed the loaded memory into the prompt
chain = (
    RunnablePassthrough.assign(
        history=lambda x: memory.load_memory_variables({})['history']
    )
    | prompt 
    | llm 
    | StrOutputParser()
)

# 5. Define Chat Helper Function
def chat(user_input: str):
    print(f"\n--- Turn ---")
    print(f"Human: {user_input}")
    
    # Invoke the chain (the history is pulled inside via RunnablePassthrough)
    response = chain.invoke({"input": user_input})
    print(f"AI: {response}")
    
    # Save context to memory so it updates for the next turn
    memory.save_context({"input": user_input}, {"output": response})
    
    # Inspect current memory state to see if it's a summary or raw messages
    print("\n[Current Memory State]")
    current_history = memory.load_memory_variables({})['history']
    for msg in current_history:
        print(f"Type: {type(msg).__name__} -> Content: {msg.content[:100]}...")
        
    return response

# 6. Execute 6 multi-turn interactions with heavy content to trigger summarization
turns = [
    "Let's talk about Quantum Computing. It uses qubits instead of classical bits.",
    "Quantum superposition allows qubits to be in multiple states simultaneously.",
    "Entanglement connects qubits so that the state of one instantly influences another.",
    "Quantum annealing is used for optimization problems, whereas universal quantum computers handle general algorithms.",
    "Companies like IBM, Google, and Rigetti are leading the hardware race using superconducting qubits.",
    "What have we discussed so far?"  # Final Turn
]

for turn in turns:
    chat(turn)