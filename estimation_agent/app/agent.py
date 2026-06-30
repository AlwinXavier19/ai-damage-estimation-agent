from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools.analyze_damage_tool import analyze_damage

import os
import google.auth

# Vertex AI configuration (required by ADK itself)
_, project_id = google.auth.default()

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


root_agent = Agent(
    name="estimation_agent",

    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(
            attempts=3
        ),
    ),

    instruction="""
You are the AI Estimation Agent.

Your only responsibility is to analyze
exactly six pre-repair images.

Always use the analyze_damage tool.

Never calculate prices.

Never calculate GST.

Never estimate labour charges.

Never modify approval workflow.

Return structured JSON only.
""",

    tools=[
        analyze_damage,
    ],
)

app = App(
    root_agent=root_agent,
    name="ai-estimation-agent",
)
