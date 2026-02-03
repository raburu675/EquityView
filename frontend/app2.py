import streamlit as st
import requests

st.title("AI Task Manager")

#user input
user_query = st.text_input("What do you need to do?", "I need to fix the login bug by tomorrow, it's super urgent.")

if st.button("Generate Task"):
    with st.spinner("AI Is thinking...."):
        # call our fastAPI backend
        response = response.post(
            "http://localhost:8000/process-task", 
            params={"user_input": user_query}
        )

        if response.status_code == 200:
            data = response.json()
            st.success("Task saved to database!")

            #Display formatted data
            st.json(data)
            st.metric(label="Priority", value=data['Priority'])
        else: 
            st.error("something went wrong")