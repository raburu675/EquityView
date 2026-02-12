import os
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def run_finance_agent(prompt: str, table_rows: list):
    # Create the DataFrame dynamically from the frontend's data
    df = pd.DataFrame(table_rows)
    
    # 1. Define Tools (Calculations) using the dynamic dataframe
    def get_total_sales() -> float:
        return float(df["Sales"].sum())

    def get_total_investment() -> float:
        return float(df["Investment"].sum())

    def get_profit(month: str = None) -> float:
        if month:
            month_clean = month.strip().capitalize()
            row = df[df["Month"] == month_clean]
            if not row.empty:
                # Profit = Sales - Investment
                return float(row["Sales"].values[0] - row["Investment"].values[0])
            return 0.0
        return float(df["Sales"].sum() - df["Investment"].sum())

    # 2. Setup Agent Tools and Context
    tools = [get_total_sales, get_total_investment, get_profit]
    context_table = df.to_string(index=False)

    system_instr = f"""
    You are a finance agent. You have access to this specific data:
    {context_table}
    
    INSTRUCTIONS:
    1. For general analysis, refer to the table.
    2. For any math/totals, you MUST use the provided tools.
    3. Every response MUST be exactly 4 lines of text.
    """

    # 3. Call Gemini
    config = types.GenerateContentConfig(
        system_instruction=system_instr,
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        config=config,
        contents=prompt
    )
    
    return response.text