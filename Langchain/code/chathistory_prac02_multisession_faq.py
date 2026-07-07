'''
Build a stateful multi-session FAQ assistant that:

Uses InMemoryChatMessageHistory with a get_session_history(session_id) factory
Uses trim_messages to keep each session's history under 300 tokens before each call
Wires everything into an LCEL chain with MessagesPlaceholder
Simulates 2 users (session_a, session_b) having completely independent conversations — at least 4 turns each
After all turns, prints both sessions' full history side by side
Asks both sessions "What have we discussed?" — each should recall only their own conversation'''




from langchain_core.chat_history import InMemoryChatMessageHistory
chat_history:dict[str,InMemoryChatMessageHistory()]

