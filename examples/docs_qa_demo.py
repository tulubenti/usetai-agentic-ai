from usetai_agentic_ai.agents.demo_agent import DemoAgent
from usetai_agentic_ai.settings import AppSettings

if __name__ == "__main__":
    agent = DemoAgent(AppSettings())
    result = agent.run(task="docs_qa", query="How do I run a quick local demo?")
    print(result["response"])
