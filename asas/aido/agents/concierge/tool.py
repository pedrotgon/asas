from google.adk.tools import AgentTool

from .agent import concierge_agent


concierge_tool = AgentTool(agent=concierge_agent)


__all__ = ["concierge_tool"]
