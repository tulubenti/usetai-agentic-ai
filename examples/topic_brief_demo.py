from usetai_agentic_ai.agents.demo_agent import DemoAgent
from usetai_agentic_ai.settings import AppSettings

if __name__ == "__main__":
    agent = DemoAgent(AppSettings())
    result = agent.run(task="topic_brief", query="autonomous agents")
    print(result["response"])
