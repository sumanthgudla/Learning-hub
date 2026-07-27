'''
Beginner — chathistory_prac01_message_store.py
Task: Create an InMemoryChatMessageHistory and:

Add a SystemMessage setting the assistant as a "Python tutor"
Simulate 3 full conversation turns using add_user_message and add_ai_message
Print all messages with their type and content
Clear the history and confirm it's empty
Print the total message count before and after clear

Expected:'''


from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory


history=InMemoryChatMessageHistory()

history.add_message(SystemMessage(content="You are an a ai assistant "))

history.add_message(HumanMessage(content="Hi"))
history.add_message(SystemMessage(content="Hello"))
history.add_message(HumanMessage(content="Hi"))
history.add_message(SystemMessage(content="Hello"))
history.add_message(HumanMessage(content="Hi"))
history.add_message(SystemMessage(content="Hello"))

for message in history.messages:
    print(f"Type: {message.type.upper():<7} | Content: {message.content}")

history.clear()
print(history)