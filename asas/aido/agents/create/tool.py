from google.adk.tools import AgentTool

from .pipeline.agent import create_pipeline


create_tool = AgentTool(agent=create_pipeline)


__all__ = ["create_tool"]
