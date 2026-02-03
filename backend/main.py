from fastapi import FastAPI
from .agent import analysis_agent, FinancialContext

app = FastAPI()

@app.post("/ask-analyst")
async def ask_analyst(question: str, data_csv: str):
    #pack the streamlit data into the agents context
    deps = FinancialContext(
        data_summary=data_csv,
        app_structure="Bar chart (Invest), Line chart (Sales), Area chart (Profit)"
    )

    #Run the Agent    
    result = await analysis_agent.run(question, deps=deps)
    return {"answer" : result.data}