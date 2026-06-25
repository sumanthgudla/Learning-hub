from langchain_core.prompts import ChatPromptTemplate


chat_template=ChatPromptTemplate.from_messages([
   ( "system","You are a {role} expert"),
    ("user","Answer this in {style} style: {question}")
])

chat_message=chat_template.invoke({"role":"python","style":"bullet points","question":"what is decorators"})
print(chat_message)