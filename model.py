from langchain_openai import ChatOpenAI
import streamlit as st

def get_openai_model():
    # Get API key from Streamlit secrets
    if not st.secrets["OPENAI_API_KEY"]:
        raise ValueError("OpenAI API key not found in Streamlit secrets")
        
    llm = ChatOpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        model="gpt-4o-mini",
        temperature=0.7
    )
    return llm