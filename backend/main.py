from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Query
from agent import run_finance_agent

app = FastAPI()

# Enable CORS so your Streamlit frontend doesn't get blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask_finance(query: Query):
    # We pass the prompt AND the data to the agent
    response_text = run_finance_agent(query.prompt, query.data)
    return {"response": response_text}

