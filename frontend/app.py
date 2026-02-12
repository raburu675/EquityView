import streamlit as st
import pandas as pd
import requests

# SET CONFIG PAGE
st.set_page_config(page_title="Company Analytics", layout="wide")

st.title("12 Month business Analysis")

# create the Dictionary
data = {
    "Month" : ["January","February","March","April","May","June","July","August","September","October","November","December"],
    "Investment" : [45000,52000,55000,53000,58000,62000,72000,60000,57000,50000,50000,40000],
    "Sales" : [120000,130750, 140900, 140100,150000,155000,210000,163000,150000,147200,138000,100000]    
}

# convert dictionary to a DataFrame
df = pd.DataFrame(data)

# 3. CALCULATE PROFIT (Sales - Investment)
df["Profit"] = df["Sales"] - df["Investment"]



# 1. Create the context HERE so it's always defined
csv_context = df.to_csv() 

# --- 🤖 AI SIDEBAR CHAT ---
with st.sidebar:
    st.header("🤖 Financial AI Assistant")
    st.markdown("---")
    
    # User input
    user_question = st.text_input("Ask a question about your data:", placeholder="e.g., What was the profit in May?")

    if st.button("Analyze"):
        if user_question:
            with st.spinner("Talking to Backend..."):
                try:
                    # 1. Prepare data: Convert DataFrame to a list of dictionaries
                    # We use reset_index() to make sure 'Month' is included if it was set as index
                    table_data = df.reset_index().to_dict(orient="records")

                    # 2. Match the Backend 'Query' model (prompt and data)
                    payload = {
                        "prompt": user_question,
                        "data": table_data
                    }

                    # 3. Send request to FastAPI
                    response = requests.post("http://localhost:8000/ask", json=payload)

                    if response.status_code == 200:
                        answer = response.json().get("response")
                        st.subheader("Analyst Response:")
                        st.info(answer)
                    else:
                        st.error(f"Backend Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
        else:
            st.warning("Please enter a question first!")

    st.markdown("---")
    st.caption("Powered by Gemini 2.0 & FastAPI")



# set the Month as the index so the charts use it as the X-axis automatically
df.set_index("Month", inplace=True)

# Display the summary table now showing profit
st.subheader("Monthly Financial Summary")
st.dataframe(df, width="stretch")

# DATA VISUALIZATION SECTION
st.divider() #adds a visual horizontal line
st.header("Financial Analysis Charts")

# create columns for a side-by-side layout
col1 , col2 = st.columns(2)

with col1:
    # chart 1: Bar chart for investment
    st.subheader("Monthly investment")
    st.bar_chart(df["Investment"], color="#ff4b4b")

with col2:
    #chart 2 line for sales trends
    st.subheader("Monthly sales")
    st.line_chart(df["Sales"], color="#29b5e8")

# Chart 3: Area chart for Profit
st.subheader("Profit Trajectory")
st.area_chart(df["Profit"], color="#29e872")


# SUMMARY METRICS
st.divider()
m_col1, m_col2, m_col3 = st.columns(3)

# Calculate totals
total_investment = df['Investment'].sum()
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

m_col1.metric("Total Investment", f"${total_investment:,}")
m_col2.metric("Total Sales", f"${total_sales:,}")
m_col3.metric("Total Profit", f"${total_profit:,}")