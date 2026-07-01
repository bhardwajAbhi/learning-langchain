from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
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
# Prompt 1
# Extract structured privacy findings from Android logs
# ----------------------------------------------------------
audit_prompt = PromptTemplate(
    input_variables=["logs"],
    template="""
    You are an Android Privacy Auditor.

    Analyze the following Android Input Monitoring logs.

    Your responsibility is ONLY to identify privacy related findings.

    Review the logs and identify:
        1. Personal Information
        2. Financial Information
        3. Authentication Secrets
        4. Device/User Identifiers
        5. User Generated Content
        6. Consent & Privacy Events

    For every finding extract:
        - type
        - value
        - activity
        - widget
        - severity

    For Consent Review determine:
        - Was a consent dialog available?
        - Which consent dialogs were shown?
        - Was a Privacy Policy shown?
        - Were Terms of Service shown?
        - Was the consent viewed?
        - Was consent accepted?
        - Was consent declined?

    Return ONLY valid JSON.

    Logs:

    {logs}

    """
)

# ----------------------------------------------------------
# Prompt 2
# Generate a privacy assessment report using the extracted
# findings from prompt 1 and selected compliance standard
# ----------------------------------------------------------
report_prompt = PromptTemplate(
    input_variables=["findings", "compliance"],
    template="""
    You are a Privacy Compliance Officer.

    The following privacy findings were extracted from Android application logs.

    Compliance Standard:

    {compliance}

    Privacy Findings:

    {findings}

    Generate a concise Privacy Assessment Report.

    Include:
        1. Executive Summary
        2. Overall Risk
        3. Sensitive Information Summary
        4. Exposed Sensitive Information (values)
        5. Consent Review
        6. Release Recommendation
        7. Developer Recommendations
    
    """
)

# ----------------------------------------------------------
# LCEL Chains
# ----------------------------------------------------------
audit_chain = audit_prompt | llm | JsonOutputParser()
report_chain = report_prompt | llm 

compliance_check_chain = (
    audit_chain
    | (lambda findings: {"findings": findings, "compliance": compliance}) 
    | report_chain
)

# ----------------------------------------------------------
# Building Streamlit UI
# ----------------------------------------------------------
st.set_page_config(page_title="Android Privacy Auditor")
st.title("Android App Privacy Compliance Check")

st.info(
    """
    This application analyzes logs to identify privacy related findings 
    such as:
    - Personal Information (PII)
    - Financial Information
    - Authentication Secrets
    - Device Identifiers
    - User Generated Content
    - Consent & Privacy Events

    The extracted findings are then reviewed against the selected
    compliance standard to generate a Privacy Assessment Report.
    """
)

logs = st.text_area(
    label="Add logs here",
    height=300, 
    placeholder="""
    Example Android Input Monitoring logs:

    07-01 10:15:25 INPUT_MONITOR_EDITTEXT window=FormLogin view=email text=[john.doe@gmail.com]

    07-01 10:15:31 INPUT_MONITOR_EDITTEXT window=FormLogin view=password text=[MyPassword123]
    """
)

compliance = st.selectbox(
    "Compliance Standard",
    [
        "GDPR",
        "DPDP",
        "HIPAA",
        "PCI DSS",
    ],
)

analyze_button = st.button(label="Analyze", use_container_width=True)
# ----------------------------------------------------------
# Generating Response
# ----------------------------------------------------------
if analyze_button:
    if logs.strip():
        with st.spinner(text="Analyzing Android logs..."):
            response = compliance_check_chain.invoke({"logs":logs})
            
        st.success("Analysis completed successfully.")

        st.subheader("Privacy Assessment Report")
        st.write(response.content)
    else:
        st.warning("Please enter the logs to continue...")



'''
----------------------------------
Sample Logs for Testing:
----------------------------------

06-30 14:07:52.982  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/code.ActivityMainMenu | widget=android.widget.LinearLayout | id=? | text=Dialogs | desc=<none>

06-30 14:07:57.586  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/code.ActivityMainMenu | widget=android.widget.LinearLayout | id=? | text=Term of Services | desc=<none>

06-30 14:08:06.899  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.dialog.DialogTermOfServices | widget=androidx.appcompat.widget.AppCompatButton | id=bt_accept | text=Accept | desc=<none>

06-30 14:08:17.064  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/code.ActivityMainMenu | widget=android.widget.LinearLayout | id=? | text=GDPR Basic | desc=<none>

06-30 14:08:22.403  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.dialog.DialogGDPRBasic | widget=androidx.appcompat.widget.AppCompatTextView | id=tv_content | text=By using this App, you agree to the Terms-Conditions, Cookies-Policy and Privacy-Policy and consent to having your personal data transferred and processed outside EU. | desc=<none>

06-30 14:08:29.298  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.dialog.DialogGDPRBasic | widget=androidx.appcompat.widget.AppCompatButton | id=bt_accept | text=ACCEPT | desc=<none>

06-30 14:08:58.886  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.form.FormLogin | view=email | hint=Email | inputType=TEXT/EMAIL_ADDRESS | text=[abhi@email.com]

06-30 14:09:16.488  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.form.FormLogin | view=password | hint=Password | inputType=TEXT/PASSWORD | text=[Abcd1234]

06-30 14:09:19.280  9398  9398 D INPUT_MONITOR_COMPOUND_BUTTON: pkg=com.material.components | window=com.material.components/com.screens.activity.form.FormLogin | widget=AppCompatCheckBox | label=Remember me | old_state=UNCHECKED | new_state=CHECKED

06-30 14:09:21.553  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.form.FormLogin | widget=androidx.appcompat.widget.AppCompatButton | id=email_sign_in_button | text=LOGIN

06-30 14:09:55.124  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.chat.ChatWhatsapp | view=text_content | hint=Write a message... | inputType=TEXT/NORMAL | text=[hello]

06-30 14:10:05.452  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.chat.ChatWhatsapp | widget=FloatingActionButton | id=btn_send | text=<none>

06-30 14:10:17.325  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.chat.ChatWhatsapp | view=text_content | hint=Write a message... | inputType=TEXT/NORMAL | text=[how are you]

06-30 14:10:19.046  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.chat.ChatWhatsapp | widget=FloatingActionButton | id=btn_send | text=<none>

06-30 14:10:40.509  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.chat.ChatWhatsapp | view=text_content | hint=Write a message... | inputType=TEXT/NORMAL | text=[I'm good]

06-30 14:10:42.714  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.chat.ChatWhatsapp | widget=FloatingActionButton | id=btn_send | text=<none>

06-30 14:10:57.600  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.payment.PaymentCardDetails | view=et_card_number | hint=Credit Card Number | inputType=NUMBER | text=[123456789874]

06-30 14:11:04.975  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.payment.PaymentCardDetails | view=et_expire | hint=MMYY | inputType=NUMBER | text=[0866]

06-30 14:11:08.953  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.payment.PaymentCardDetails | view=et_cvv | hint=CVV | inputType=NUMBER | text=[302]

06-30 14:11:22.104  9398  9398 D INPUT_MONITOR_EDITTEXT: pkg=com.material.components | window=com.material.components/com.screens.activity.payment.PaymentCardDetails | view=et_name | hint=Name on Card | inputType=TEXT | text=[testName]

06-30 14:11:24.655  9398  9398 D INPUT_MONITOR_CLICK: pkg=com.material.components | window=com.material.components/com.screens.activity.payment.PaymentCardDetails | widget=androidx.appcompat.widget.AppCompatButton | id=btn_continue | text=CONTINUE
'''