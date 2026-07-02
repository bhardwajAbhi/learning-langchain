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
""",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# ----------------------------------------------------------
# LCEL Chain with Conversation History
# ----------------------------------------------------------
chain = prompt | llm

history = StreamlitChatMessageHistory()

chat_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,
    history_messages_key="chat_history",
    input_messages_key="input",
)

# ----------------------------------------------------------
# Building Streamlit UI
# ----------------------------------------------------------
st.set_page_config(page_title="Android Security Assistant")

st.title("Android Security Assistant")

st.caption(
    "Ask questions about Android Security, Secure Coding, Android Internals, "
    "OWASP Mobile Top 10, Malware Analysis, Privacy and Reverse Engineering."
)

# ----------------------------------------------------------
# Display Previous Conversation
# ----------------------------------------------------------

for message in st.session_state["langchain_messages"]:

    role = "user" if message.type == "human" else "assistant"

    with st.chat_message(role):
        st.markdown(message.content)

# ----------------------------------------------------------
# Chat Input
# ----------------------------------------------------------

question = st.chat_input(
    "Ask anything about Android Security..."
)

# ----------------------------------------------------------
# Generating Response
# ----------------------------------------------------------

if question:

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chat_with_history.stream(
                {"input": question},
                config={
                    "configurable": {
                        "session_id": "any"
                    }
                },
            )

            st.write_stream(response)