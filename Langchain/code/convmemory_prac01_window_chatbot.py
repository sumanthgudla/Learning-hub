'''
Beginner — convmemory_prac01_window_chatbot.py
Task: Build a simple chatbot using ConversationBufferWindowMemory with k=3. Simulate 5 conversation turns manually using save_context(). After all 5 turns, print the memory contents and verify only the last 3 turns are present.
Expected:
Memory after 5 turns:
HumanMessage: "Turn 3 input"
AIMessage:    "Turn 3 output"
HumanMessage: "Turn 4 input"
AIMessage:    "Turn 4 output"
HumanMessage: "Turn 5 input"
AIMessage:    "Turn 5 output"
'''

from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate

prompt_message=ChatPromptTemplate(
    [
        ('system','you are an ai asssitant'),
        ('user','hi')
    ]
)

memory=ConversationBufferWindowMemory(
    k=3,
    return_messages=True,
    memory_key='history'

)

for i in range(10):
    memory.save_context(
        {"input":"hi"},
        {"output":"hello"}
    )
chat_memory=memory.load_memory_variables({})['history']

for i in chat_memory:
    print(i.content)