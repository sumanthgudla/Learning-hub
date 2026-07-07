Check your network Connection.

×
Back
LangChain Mastery
7 Chapter(s)
109 Lesson(s)
16%
Search lessons
1.
LangChain Basics
2.
Chains
What is a chain in LangChain, and how is it used in NLP?
How do you create a sequential chain in LangChain?
What is the difference between LLMChain and SequentialChain?
How do you pass inputs to a LangChain chain?
What is the role of output parsers in LangChain chains?
How do you debug a LangChain chain?
Write a function to create a LangChain chain for question answering.
How do you implement a chain with multiple prompts in LangChain?
Write a function to chain text generation and parsing.
How do you use LangChain to create a conversational chain?
Implement a chain to handle batch processing in LangChain.
How do you handle errors in LangChain chains?
Write a function to implement a custom LangChain chain.
How do you optimize LangChain chains for low-latency NLP tasks?
Write a function to implement a parallel chain execution in LangChain.
How do you implement a chain with dynamic routing in LangChain?
Implement a chain to handle multi-step reasoning in LangChain.
3.
Agents and Tools
4.
Memory
5.
Retrieval and Vector Stores
6.
Debugging and Error Handling
7.
Best Practices and Optimization
How do you pass inputs to a LangChain chain?
How do you pass inputs to a LangChain chain?
Passing inputs to a LangChain chain means giving it the data it needs to generate a response.

In simple terms:

You create a chain with placeholders.
Then you provide values for those placeholders when calling the chain.

First, understand that most chains expect input as a dictionary.

The keys of the dictionary must match the variable names in the prompt.

Let’s see a basic example.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

chain = prompt | llm

Here, the prompt contains {topic}.

That means the chain expects an input variable named "topic".

Now we pass input like this:

response = chain.invoke({"topic": "machine learning"})
print(response.content)

Important:

The key "topic" must match the placeholder {topic}.

If it does not match, the chain will raise an error.


Now let’s look at multiple inputs.

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in a {tone} tone."
)

chain = prompt | llm

response = chain.invoke({
    "topic": "neural networks",
    "tone": "funny"
})

print(response.content)

Here we pass two values:

topic

tone

Both must be provided.


There are different ways to pass inputs depending on the situation.

1. Using .invoke() (Most Common)
chain.invoke({"topic": "AI"})

This is recommended for modern LangChain (LCEL).


2. Using .run() (Older style)
If using LLMChain:

result = chain.run("AI")

This works only when there is one input variable.

If there are multiple inputs, you must use a dictionary:

result = chain.run({"topic": "AI", "tone": "simple"})


3. Batch inputs
You can process multiple inputs at once:

responses = chain.batch([
    {"topic": "AI"},
    {"topic": "blockchain"},
    {"topic": "cloud computing"}
])

This is useful for:

Bulk processing

Reducing latency

Cost optimization


4. Streaming input
If streaming is enabled:

for chunk in chain.stream({"topic": "AI"}):
    print(chunk.content, end="")

This returns tokens as they are generated.


Now let’s understand the key rule clearly.

The prompt defines required input variables.
You must pass those variables as a dictionary when calling the chain.
Input variables → Dictionary keys
Values → Dictionary values

No material available!
The trainer has not added any training content or tests to this lesson yet. Once the trainer adds content or tests, they will be displayed here.