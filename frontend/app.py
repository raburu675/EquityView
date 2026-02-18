import streamlit as st
import pandas as pd
import requests

# 1. INITIAL SETUP & SECRETS
st.set_page_config(page_title="Company Analytics", layout="wide")

# Fetch Backend URL from Streamlit Cloud Secrets (added previously)
# Falls back to localhost for your local testing
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

# 2. HELPER FUNCTION: Handle Render's "Sleep" mode
def check_backend():
    try:
        # Pings the root of your FastAPI app on Render
        response = requests.get(BACKEND_URL, timeout=3)
        return response.status_code == 200
    except:
        return False

st.title("12 Month business Analysis")

# UI Warning for users if Render is still booting up
if not check_backend():
    st.warning("ℹ️ The AI backend is waking up... please wait about 30 seconds.")

# create the Dictionary
data = {
    "Month" : ["January","February","March","April","May","June","July","August","September","October","November","December"],
    "Investment" : [45000,52000,55000,53000,58000,62000,72000,60000,57000,50000,50000,40000],
    "Sales" : [120000,130750, 140900, 140100,150000,155000,210000,163000,150000,147200,138000,100000]    
}

# convert dictionary to a DataFrame
df = pd.DataFrame(data)

# 3. CALCULATE PROFIT
df["Profit"] = df["Sales"] - df["Investment"]

# --- 🤖 AI SIDEBAR CHAT ---
with st.sidebar:
    st.header("🤖 Financial AI Assistant")
    st.markdown("---")
    
    user_question = st.text_input("Ask a question about your data:", placeholder="e.g., What was the profit in May?")

    if st.button("Analyze"):
        if user_question:
            with st.spinner("Talking to Backend..."):
                try:
                    # Convert DataFrame to a format the AI can read
                    table_data = df.to_dict(orient="records")

                    payload = {
                        "prompt": user_question,
                        "data": str(table_data) # Convert to string for the agent
                    }

                    # Call your Render URL /ask endpoint
                    response = requests.post(f"{BACKEND_URL}/ask", json=payload)

                    if response.status_code == 200:
                        answer = response.json().get("response")
                        st.subheader("Analyst Response:")
                        st.info(answer)
                    else:
                        st.error(f"Backend Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"Connection Failed: Ensure your Render backend is Live.")
        else:
            st.warning("Please enter a question first!")

    st.markdown("---")
    st.caption("Powered by Gemini 2.0 & FastAPI")

# Prepare chart data
chart_df = df.set_index("Month")

# Display the summary table
st.subheader("Monthly Financial Summary")
st.dataframe(df, width="stretch") # Kept your original 'stretch' setting

# DATA VISUALIZATION SECTION
st.divider()
st.header("Financial Analysis Charts")

col1 , col2 = st.columns(2)

with col1:
    st.subheader("Monthly investment")
    st.bar_chart(chart_df["Investment"], color="#ff4b4b")

with col2:
    st.subheader("Monthly sales")
    st.line_chart(chart_df["Sales"], color="#29b5e8")

st.subheader("Profit Trajectory")
st.area_chart(chart_df["Profit"], color="#29e872")

# SUMMARY METRICS
st.divider()
m_col1, m_col2, m_col3 = st.columns(3)

total_investment = df['Investment'].sum()
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

m_col1.metric("Total Investment", f"${total_investment:,}")
m_col2.metric("Total Sales", f"${total_sales:,}")
m_col3.metric("Total Profit", f"${total_profit:,}")