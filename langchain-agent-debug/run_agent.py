"""Run the demo agent from the command line.

Usage:
  1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
  2. Install dependencies from `requirements.txt`.
  3. Run: `python run_agent.py` and type a task.
"""

from dotenv import load_dotenv
import os

load_dotenv()

from langchain.llms import OpenAI
from langchain.llms import AzureOpenAI
from callback_handler import StepByStepCallbackHandler
from agent import SimpleAgent


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY in your environment (see .env.example)")
        return

    # Support either OpenAI or Azure OpenAI based on environment variables.
    use_azure = os.getenv("USE_AZURE", "").lower() == "true" or os.getenv(
        "AZURE_OPENAI_API_BASE"
    )

    if use_azure:
        deployment = os.getenv("AZURE_DEPLOYMENT_NAME") or os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        )
        if not deployment:
            print(
                "Azure detected but no deployment name set. Set AZURE_DEPLOYMENT_NAME in .env"
            )
            return
        llm = AzureOpenAI(deployment_name=deployment, temperature=0)
    else:
        llm = OpenAI(temperature=0)
    cb = StepByStepCallbackHandler()
    agent = SimpleAgent(llm, cb)

    print("Simple LangChain-style agent (debug mode). Type your task:")
    user_input = input("Task> ")
    final = agent.run(user_input)
    print("\n=== FINAL ANSWER ===")
    print(final)


if __name__ == "__main__":
    main()
