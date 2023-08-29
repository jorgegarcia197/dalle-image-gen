import streamlit as st
import numpy as np
import openai
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_type = "azure"
openai.api_base = os.environ.get("OPENAI_API_BASE")
openai.api_version = os.environ.get("OPENAI_API_VERSION")

ASSISTANT_PATH = "assets/assistant.png"
USER_PATH = "assets/users_white.png"


import openai
import streamlit as st

st.set_page_config(
        page_title="DALL-E Image Generator", page_icon="🎨", layout="wide"
    )
st.image('assets/InnovationLogoDark.png')

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    number_of_images = st.number_input("Number of images", min_value=1, max_value=6, value=1, step=1)
    image_size = st.selectbox("Image size", options=["256", "512", "1024"], index=0)
    
st.title("💬 DALL-E Image Generator")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"],avatar=USER_PATH).write(msg["content"])
    elif msg["role"] == "assistant" and msg["content"] == "How can I help you?":
        st.chat_message(msg["role"],avatar=ASSISTANT_PATH).write(msg["content"])
    else:
        st.chat_message("assistant",avatar=ASSISTANT_PATH).image(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user",avatar=USER_PATH).write(prompt)
    response = openai.Image.create(
    prompt=prompt,
    size=f'{image_size}x{image_size}' if image_size else '1024x1024',
    n=number_of_images if number_of_images else 1
    )
    urls = [response.get('data')[i].get('url') for i in range(number_of_images)]
    st.session_state.messages.append({"role": "assistant", "content": urls})
    images = [url for url in urls]
    st.chat_message("assistant",avatar=ASSISTANT_PATH).image(images)


