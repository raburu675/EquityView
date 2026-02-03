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



# 🤖 AI SIDEBAR CHAT
with st.sidebar:
    st.header("🤖 Financial AI Assistant")
    st.write("Ask questions about the data below!")

    user_question = st.text_input("Message the Analyst:")

    if user_question:
        #convert our dataframe to a string for the AI to read
        csv_context = df.to_csv()

        #2. send to FastAPI
        with st.spinner("Analyzing....."):
            response = requests.post(
                "http://localhost:8000/ask-analyst",
                params={"question": user_question, "data_csv": csv_context}
            )

            if response.status_code == 200:
                st.info(response.json()["answer"])
            else:
                st.error("AI is offline. Ensure FastAPI is running.")





# set the Month as the index so the charts use it as the X-axis automatically
df.set_index("Month", inplace=True)

# Display the summary table now showing profit
st.subheader("Monthly Financial Summary")
st.dataframe(df, use_container_width=True)

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