import streamlit as st
from google import genai
from app.Utils.sidebar import render_sidebar

# Hide default multipage navigation
hide_default_pages = """
<style>
div[data-testid="stSidebarNav"] ul {display: none !important;}
div[data-testid="stSidebarNav"] h2 {display: none !important;}
</style>
"""
st.markdown(hide_default_pages, unsafe_allow_html=True)

# Render shared sidebar
render_sidebar()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.subheader("Gemini API")

# INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY EXISTING MESSAGES
for message in st.session_state.messages:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# USER INPUT
prompt = st.chat_input("Type here")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    # SEND TO GEMINI
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=st.session_state.messages
    )

    # STREAM ASSISTANT RESPONSE
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""

        for chunk in response:
            if chunk.text:
                full_reply += chunk.text
                container.markdown(full_reply)

    # SAVE ASSISTANT MESSAGE
    st.session_state.messages.append({
        "role": "model",
        "parts": [{"text": full_reply}]
    })



