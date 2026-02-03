import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

# 1. Load the keys
load_dotenv()
# Mapping your key to the one PydanticAI expects
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

@dataclass
class FinancialContext:
    data_summary: str 
    app_structure: str 

# 2. Initialize the Agent with the newest model
analysis_agent = Agent(
    'google-gla:gemini-2.0-flash', # Upgraded to 2.0
    deps_type=FinancialContext,
    # result_type=str, # Optional: Define if you want a Pydantic model back
    system_prompt=(
        "You are a Business Intelligence Assistant for 'Company Analytics'. "
        "You have access to a 12-month financial dataset. "
        "Use the provided context to answer user questions accurately. "
        "Always refer to specific charts when relevant: "
        "- 'Monthly Investment' (Bar Chart) "
        "- 'Monthly Sales' (Line Chart) "
        "- 'Profit Trajectory' (Area Chart)"
    )
)

# 3. Dynamic system prompt (Corrected typo in 'system_prompt')
@analysis_agent.system_prompt
def add_data_to_prompt(ctx: RunContext[FinancialContext]) -> str:
    return (
        f"CONTEXT DATA:\n{ctx.deps.data_summary}\n\n"
        f"APP LAYOUT:\n{ctx.deps.app_structure}"
    )