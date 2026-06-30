from langchain_ollama.chat_models import ChatOllama
import streamlit as st

llm = ChatOllama(model="mistral")

st.title("Ollama Chat with Streamlit")

query = st.text_input("Enter your query")

if query:
    response = llm.invoke(query)
    st.write(response.content)
