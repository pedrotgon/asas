from google.adk.tools import AgentTool

from .pipeline.agent import update_pipeline


update_tool = AgentTool(agent=update_pipeline)


__all__ = ["update_tool"]
