import time


class StepByStepCallbackHandler:
    """Simple, explicit callback-like handler that logs each agent step.

    Methods are lightweight and called from the agent implementation below.
    """

    def _log(self, tag: str, message: str):
        print(f"[{time.strftime('%H:%M:%S')}] {tag}: {message}")

    def on_chain_start(self, info: dict):
        self._log("CHAIN START", f"Starting chain with input: {info.get('input')}")

    def on_llm_start(self, info: dict):
        self._log("LLM CALL", f"Prompt sent to LLM: {info.get('prompt')}")

    def on_llm_end(self, info: dict):
        self._log("LLM RESP", f"LLM returned: {info.get('response')}")

    def on_tool_start(self, info: dict):
        self._log("TOOL START", f"Calling tool '{info.get('tool')}' with input: {info.get('input')}")

    def on_tool_end(self, info: dict):
        self._log("TOOL END", f"Tool '{info.get('tool')}' returned: {info.get('output')}")

    def on_chain_end(self, info: dict):
        self._log("CHAIN END", f"Chain finished. Final answer: {info.get('final_answer')}")
