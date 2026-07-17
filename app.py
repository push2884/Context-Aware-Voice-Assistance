import streamlit as st
from langchain_openai import ChatOpenAI
import httpx
import json

# ----------------------------
# Configure Page
# ----------------------------
st.set_page_config(
    page_title="PrivacyShield AI",
    page_icon="🔒",
    layout="wide"
)

# ----------------------------
# Connect to GPT-4o
# ----------------------------
client = httpx.Client(verify=False)

llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o",
    api_key="sk-LUN1OjfXBHi9IwljISMkag",
    http_client=client,
    temperature=0
)

# ----------------------------
# UI
# ----------------------------

st.title("🔒 PrivacyShield AI")
st.subheader("Context-Aware Privacy Protection")

st.write(
    """
This prototype detects whether a user's request contains sensitive
information and decides whether the assistant should respond aloud
based on the surrounding environment.
"""
)

environment = st.selectbox(
    "🌍 Select Current Environment",
    [
        "Home",
        "Office",
        "Cafe",
        "Restaurant",
        "Metro",
        "Airport",
        "Bus",
        "Train"
    ]
)

query = st.text_area(
    "💬 Enter the user's spoken request",
    placeholder="Example: What is my account balance?"
)

# ----------------------------
# Analyze Button
# ----------------------------

if st.button("Analyze Privacy"):

    if query.strip() == "":
        st.warning("Please enter a query.")
        st.stop()

    prompt = f"""
You are PrivacyShield AI.

Your task is to analyze whether the user's request
contains privacy-sensitive information.

Environment:
{environment}

User Query:
{query}

Sensitive Categories:

- Banking
- OTP
- Password
- Medical
- Aadhaar
- PAN
- Salary
- Credit Card
- Debit Card
- Personal Address
- Insurance

Rules:

1. If environment is
Metro
Airport
Restaurant
Bus
Train

AND request is sensitive

Decision = HIDE

2. If environment is Home or Office

Decision = SPEAK

Return ONLY valid JSON.

Example:

{{
    "environment":"Metro",
    "risk":"HIGH",
    "decision":"HIDE",
    "privacy_score":92,
    "reason":"Sensitive banking information in a public place.",
    "assistant_response":"For your privacy, your account information has been securely displayed instead of spoken aloud."
}}

"""

    with st.spinner("Analyzing..."):

        response = llm.invoke(prompt)

    try:

        result = json.loads(response.content)

        st.success("Analysis Complete")

        col1, col2 = st.columns(2)

        with col1:

            st.metric("Environment", result["environment"])

            st.metric("Risk", result["risk"])

            st.metric(
                "Privacy Score",
                str(result["privacy_score"])
            )

        with col2:

            st.metric(
                "Decision",
                result["decision"]
            )

            st.write("### Reason")

            st.info(result["reason"])

        st.divider()

        st.subheader("🤖 Assistant Response")

        if result["decision"] == "HIDE":

            st.error(result["assistant_response"])

        else:

            st.success(result["assistant_response"])

    except Exception:

        st.error("Model Output")

        st.write(response.content)