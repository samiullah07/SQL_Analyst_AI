import streamlit as st
from main import get_data_from_db
st.set_page_config(
    page_title="Data Analyst Database",
    page_icon="📊"
    ,
)

st.title("📊 Data Analyst Database with LLM-Powered SQL Generation")
st.markdown("""
Welcome to the Data Analyst Database application! This app leverages a pre-populated SQLite database """)

query = st.text_area("Enter your natural language query here:")

if st.button("Analyze"):
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Generate Response..."):
            database_response = get_data_from_db(query)
            fixed_answer = f"Here is the generated SQL query based on your input:\n\n{database_response or 'No response generated'}"
            st.success("Response Generated!")
            st.markdown(fixed_answer)

st.markdown("---")