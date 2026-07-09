from typing import Callable, List
from langchain.llms.base import LLM
from callback_handler import StepByStepCallbackHandler
from tools import run_tool_by_name


class SimpleAgent:
    """A minimal "agent" that uses a LangChain LLM and synchronous tools.

    The agent instructs the LLM to either return a final answer or to request
    a tool call in this exact format:

    ACTION: <tool_name>
    INPUT: <input string for tool>

    Or a final answer as:
    FINAL ANSWER: <your answer>
    """

    def __init__(self, llm: LLM, callback: StepByStepCallbackHandler):
        self.llm = llm
        self.callback = callback

    def _build_prompt(self, user_input: str, history: str = "") -> str:
        return (
            "You are an assistant that either returns a final answer or requests "
            "a tool call using the exact lines:\nACTION: <tool_name>\nINPUT: <input>\n"
            "If you have the answer, return:\nFINAL ANSWER: <answer>\n\n"
            "User task: "
            + user_input
            + ("\nPrevious tool outputs:\n" + history if history else "")
        )

    def run(self, user_input: str, max_steps: int = 6) -> str:
        history = ""
        self.callback.on_chain_start({"input": user_input})

        for step in range(max_steps):
            prompt = self._build_prompt(user_input, history)
            self.callback.on_llm_start({"prompt": prompt})
            # call the LangChain LLM; it should return a plain string
            llm_response = self.llm(prompt)
            self.callback.on_llm_end({"response": llm_response})

            # quick parsing rules: look for FINAL ANSWER or ACTION/INPUT block
            low = llm_response.strip()
            if "FINAL ANSWER:" in low:
                final = low.split("FINAL ANSWER:", 1)[1].strip()
                self.callback.on_chain_end({"final_answer": final})
                return final

            # find ACTION and INPUT
            action = None
            action_input = None
            for line in low.splitlines():
                if line.strip().upper().startswith("ACTION:"):
                    action = line.split(":", 1)[1].strip()
                if line.strip().upper().startswith("INPUT:"):
                    action_input = line.split(":", 1)[1].strip()

            if action:
                self.callback.on_tool_start({"tool": action, "input": action_input})
                tool_output = run_tool_by_name(action, action_input)
                self.callback.on_tool_end({"tool": action, "output": tool_output})
                # append to history so LLM can see results and continue reasoning
                history += f"\n[{action} output]: {tool_output}\n"
                continue

            # If no recognizable structure, return the raw response
            self.callback.on_chain_end({"final_answer": llm_response})
            return llm_response
