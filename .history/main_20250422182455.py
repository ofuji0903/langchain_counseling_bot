# main.py
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from graph import app  # ← Graphは別ファイルで定義

st.set_page_config(page_title="カウンセリングチャットボット v3", page_icon="💬")
st.title("カウンセリングチャットボット v3")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("あなたの話したいことを自由に書いてください:")

if user_input:
    conversation_history = [msg[0] for msg in st.session_state.history]
    result = app.invoke({
        "user_input": user_input,
        "conversation_history": conversation_history
    })
    response = result["response"]

    st.session_state.history.append((user_input, response))

    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(response)

if st.session_state.history:
    st.markdown("---")
    st.markdown("#### 過去の会話")
    for user_msg, bot_msg in reversed(st.session_state.history[-5:]):
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(bot_msg)
