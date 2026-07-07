A PromptTemplate is a prompt with placeholders that you fill later.

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} to a {audience} using a real-life example."
)

formatted_prompt = prompt.format(topic="APIs", audience="beginner")
print(formatted_prompt)

Code explanation:

from_template(...) creates a prompt with placeholders {topic} and {audience}.
.format(...) replaces placeholders with real values.
This helps you reuse the same prompt structure for many different inputs.
