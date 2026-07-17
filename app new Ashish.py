import streamlit as st
from langchain_openai import ChatOpenAI
import httpx
import json
import os
import uuid
import tempfile
import pyttsx3
import speech_recognition as sr


# =====================================================
# Load Financial Assessment Data
# =====================================================

def load_financial_data():

    try:

        with open(
            "Financial_Assessment.txt",
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except FileNotFoundError:

        return "Financial assessment data not found."


financial_data = load_financial_data()



# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="PrivacyShield AI",
    page_icon="🔒",
    layout="wide"
)



# =====================================================
# GPT-4o Connection
# =====================================================

client = httpx.Client(
    verify=False
)


llm = ChatOpenAI(

    base_url="https://genailab.tcs.in",

    model="azure/genailab-maas-gpt-4o",

    api_key="sk-LUN1OjfXBHi9IwljISMkag",

    http_client=client,

    temperature=0
)



# =====================================================
# Voice Input
# =====================================================

def speech_to_text():

    import sounddevice as sd
    from scipy.io.wavfile import write
    import speech_recognition as sr


    sample_rate = 16000
    duration = 5


    st.info("🎙️ Listening... Speak now")


    try:

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )


        sd.wait()


        audio_file = "user_voice.wav"


        write(
            audio_file,
            sample_rate,
            recording
        )


        recognizer = sr.Recognizer()


        with sr.AudioFile(audio_file) as source:

            audio = recognizer.record(source)



        text = recognizer.recognize_google(
            audio
        )


        return text



    except sr.UnknownValueError:

        return "Unable to understand voice"



    except sr.RequestError:

        return "Speech recognition service unavailable"



    except Exception as e:

        return f"Voice input error: {str(e)}"





# =====================================================
# Text To Speech
# =====================================================

def speak_text(text):


    filename = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ).name



    engine = pyttsx3.init()


    engine.setProperty(
        "rate",
        150
    )


    engine.save_to_file(
        text,
        filename
    )


    engine.runAndWait()



    with open(
        filename,
        "rb"
    ) as audio:


        audio_bytes = audio.read()



    os.remove(
        filename
    )


    return audio_bytes




# =====================================================
# UI
# =====================================================


st.title(
    "🔒 PrivacyShield AI"
)


st.subheader(
    "Context-Aware Voice Privacy Protection"
)



st.write(
"""
PrivacyShield AI analyzes voice requests,
detects privacy risks based on environment,
and prevents sensitive information leakage.
"""
)



environment = st.selectbox(

    "🌍 Select Environment",

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



# =====================================================
# Voice Input Section
# =====================================================

st.subheader(
    "🎤 Voice Query Input"
)



if st.button(
    "Start Recording"
):


    voice_text = speech_to_text()


    st.session_state["query"] = voice_text




query = st.session_state.get(
    "query",
    ""
)



query = st.text_area(

    "Recognized Query",

    value=query

)





# =====================================================
# Analyze Button
# =====================================================


if st.button(
    "🔍 Analyze Privacy"
):


    if query.strip()=="":


        st.warning(
            "Please provide a query"
        )

        st.stop()



    prompt = """

You are PrivacyShield AI.

Analyze user request privacy risk.

Financial Assessment Data:

""" + financial_data + """

Current Environment:

""" + environment + """

User Query:

""" + query + """

Rules:

1. Use only financial assessment data.

2. Sensitive information includes:

- Account balance
- Revenue
- Profit
- Debt
- Financial statements
- Confidential financial details


3. Public environments:

Metro
Airport
Bus
Train
Cafe
Restaurant


If sensitive information is requested in public environment:

decision = HIDE


Do not reveal information.


4. Private environments:

Home
Office


decision = SHOW


Return ONLY JSON.

Format:

{
"environment":"",
"risk":"",
"decision":"",
"privacy_score":0,
"reason":"",
"assistant_response":""
}

"""



    with st.spinner(
        "Analyzing..."
    ):


        response = llm.invoke(
            prompt
        )



    try:


        clean_response = response.content.strip()



        if clean_response.startswith(
            "```"
        ):


            clean_response = clean_response.replace(
                "```json",
                ""
            )

            clean_response = clean_response.replace(
                "```",
                ""
            )

            clean_response = clean_response.strip()



        result = json.loads(
            clean_response
        )



        st.success(
            "Analysis Completed"
        )



        col1,col2 = st.columns(2)



        with col1:


            st.metric(
                "Environment",
                result["environment"]
            )


            st.metric(
                "Risk",
                result["risk"]
            )


            st.metric(
                "Privacy Score",
                result["privacy_score"]
            )



        with col2:


            st.metric(
                "Decision",
                result["decision"]
            )


            st.write(
                "### Reason"
            )


            st.info(
                result["reason"]
            )



        st.divider()



        st.subheader(
            "🤖 Assistant Response"
        )



        answer = result["assistant_response"]



        if result["decision"]=="HIDE":


            st.error(
                answer
            )


            st.warning(
                "🔇 Voice disabled to protect privacy"
            )



        else:


            st.success(
                answer
            )


            st.write(
                "### 🔊 Voice Output"
            )


            audio = speak_text(
                answer
            )


            st.audio(
                audio,
                format="audio/wav"
            )




    except Exception as e:


        st.error(
            "Model response parsing failed"
        )


        st.write(
            response.content
        )


        st.write(
            e
        )
