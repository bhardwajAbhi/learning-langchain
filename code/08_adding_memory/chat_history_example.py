from langchain_ollama.chat_models import ChatOllama

# Adding history / memory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.globals import set_debug
import streamlit as st

# ----------------------------------------------------------
# Enable LCEL Debug Logs
# ----------------------------------------------------------
set_debug(True)

# ----------------------------------------------------------
# Loading Ollama Model
# ----------------------------------------------------------
llm = ChatOllama(model="gemma:2b")

# ----------------------------------------------------------
# Prompt 
# ----------------------------------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
            """
            You are an Android Security and Secure Coding Assistant.

            You help developers understand:
            - Android Security
            - Secure Coding Practices
            - Android Internals
            - Android Security Model
            - Mobile Malware
            - OWASP Mobile Top 10
            - Privacy
            - Reverse Engineering
            - Android Architecture

            Use the previous conversation to understand follow-up questions.

            Keep your answers concise and technical.
            """
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)


# ----------------------------------------------------------
# LCEL Chain with conversation history (memory)
# ----------------------------------------------------------
chain = prompt | llm

history = StreamlitChatMessageHistory()

chat_with_history = RunnableWithMessageHistory(
    chain, 
    lambda session_id:history,
    history_messages_key="chat_history",
    input_messages_key="input",
)

# ----------------------------------------------------------
# Building Streamlit UI
# ----------------------------------------------------------
st.set_page_config(page_title="Android Security Assistant")

st.title("Android Security Assistant")

col1, col2 = st.columns([6, 1])

with col1:
    question = st.text_input(
        label="Ask a question",
        label_visibility="collapsed",
        placeholder="Ask anything about Android security..."
    )

with col2:
    ask_button = st.button(label="Send", use_container_width=True)

# ----------------------------------------------------------
# Generating Response
# ----------------------------------------------------------
if ask_button and question.strip():
    with st.spinner("Thinking..."):
        response = chat_with_history.invoke(
            {"input": question},
            config={"configurable": {"session_id": "any"}}
        )
    
    st.subheader("Answer")
    st.success(response.content)
    st.divider()

    # Chat history
    st.subheader("History")
    for message in st.session_state["langchain_messages"]:
        if message.type == "human":
            st.warning("Question: " + message.content)
        else:
            st.info("Answer: " + message.content)
        
    st.divider()