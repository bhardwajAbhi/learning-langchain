from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
import streamlit as st

# ---------------------------
# Prompt Template
# ---------------------------
prompt = PromptTemplate(
    input_variables=["permission", "audience_level", "detail_level", "language"],
    template="""
    You are an Android Security Expert with 15 years of experience in the domain.
    Explain the following Android permission:
    {permission}

    Your explanation must include:
    1. What the permission does.
    2. Its protection level (Normal, Dangerous, Signature, System, etc.).
    3. Common legitimate use cases.
    4. Potential security or privacy risks.
    5. Best practices for developers.


    Target Audience Level:
    {audience_level}

    Detail Level:
    {detail_level}

    Answer in {language}.
    """
)

# ---------------------------
# Loading Ollama Model
# ---------------------------
llm = ChatOllama(model="gemma:2b")

# ---------------------------
# Building Streamlit UI
# ---------------------------
st.set_page_config(page_title="Android Permission Explainer")

permission = st.text_input("Android Permission", placeholder="Example: READ_CONTACTS")

audience_level = st.selectbox(
    label="Audience",
    options=["Beginner", "Intermediate", "Advanced"],
    index=None,
    placeholder="Select Audience Level"
)

detail_level = st.selectbox(
    label="Detail Level",
    options=["Short", "Medium", "Detailed"],
    index=None,
    placeholder="Select Detail Level"
)

language = st.text_input(label="Language", value="English")


# ---------------------------
# Generating Response
# ---------------------------
if st.button(label="Explain Permission"):
    if permission:
        with st.spinner("Generating response..."):
            response = llm.invoke(
                prompt.format(
                    permission=permission,
                    audience_level=audience_level,
                    detail_level=detail_level,
                    language=language,
                )
            )
        st.subheader("Explanation")
        st.write(response.content)
    else:
        st.warning("Please enter a valid Android permission.")