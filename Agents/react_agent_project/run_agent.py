import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from react_agent_project.agent import run_react_agent


if __name__ == '__main__':
    result = run_react_agent('What is sum of weather in vizag and goa')
    print(result)
