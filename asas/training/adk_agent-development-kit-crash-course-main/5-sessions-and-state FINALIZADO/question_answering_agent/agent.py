from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

load_dotenv()

model = LiteLlm(model="azure/gpt-5-nano")
# Create the root agent
question_answering_agent = LlmAgent(
    name="question_answering_agent",
    model=model,
    description="Question answering agent",
    instruction="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is some information about the user:
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
)
