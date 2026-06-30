from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug

import streamlit as st

# ------------------------------------------------------
# Enable LCEL Debug Logs
# ------------------------------------------------------
set_debug(True)

# ------------------------------------------------------
# Loading Ollama Model
# ------------------------------------------------------
llm = ChatOllama(model="gemma:2b")

# ------------------------------------------------------
# Prompt 1
# Android Malware Behaviour --> Mobile ATT&CK Mapping
# ------------------------------------------------------
mitre_prompt = PromptTemplate(
    input_variables=["behavior"],
    template="""
    You are a senior Android Malware Analyst with 15 years of experience in the domain.
    Analyze the following observed Android malware behavior.
    {behavior}

    Your task is to map the behavior ONLY to the MITRE ATT&CK Mobile Matrix (Android platform).

    For every matching technique, provide:
    - Technique ID
    - Technique Name
    - One-line justification
    """
)

# ------------------------------------------------------
# Prompt 2
# Mobile ATT&CK Mapping --> Threat Intelligence Report
# ------------------------------------------------------
report_prompt = PromptTemplate(
    input_variables=["techniques"],
    template="""
    You are a Mobile Threat Intelligence Analyst.

    Below are the mapped MITRE ATT&CK Mobile techniques.
    {techniques}

    Generate a professional Android Threat Intelligence Report.

    Include the following sections:

    1. Executive Summary

    2. Mobile ATT&CK Techniques

    3. Possible Malware Objectives

    4. Detection Opportunities

    5. Mitigation Recommendations

    Keep the report concise, clear and easy to understand.
    """
)

# ---------------------------
# LCEL Chains
# ---------------------------
first_chain = mitre_prompt | llm | StrOutputParser()

second_chain = report_prompt | llm

overall_chain = first_chain | second_chain

# ---------------------------
# Building Streamlit UI
# ---------------------------
st.set_page_config(page_title="Android Mobile ATT&CK Mapper", page_icon="🤖")

st.write(
    "Describe the observed Android malware behavior. "
    "This application will first map the behavior to the **MITRE ATT&CK Mobile Matrix**, "
    "then generate a threat intelligence report."
)

behavior = st.text_area(
    label="Observed Android Malware Behavior",
    height=400, 
    placeholder="""

    App uses following permissions:
    READ_SMS
    INTERNET
    RECEIVE_BOOT_COMPLETED

    Observed Behaviour:
    - Reads incoming OTP SMS messages
    - Starts automatically after device reboot
    - Sends collected SMS messages to a remote server
    - Requests SMS permissions during installation
    - Hides app icon from the app drawer
    """
)
analyze_button = st.button(label="Analyze Behavior",)
# ---------------------------
# Generating Response
# ---------------------------
if analyze_button:
    if behavior.strip():
        with st.spinner(text="Analyzing malware behavior..."):
            response = overall_chain.invoke({"behavior":behavior})
        st.subheader("Threat Intelligence Report")
        st.write(response.content)
    else:
        st.warning("Please enter the observed Android malware behavior.")