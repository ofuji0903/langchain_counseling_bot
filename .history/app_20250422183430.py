import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from graph import app

st.set_page_config(
    page_title="カウンセリングチャットボット v3",
    page_icon="💬",
    layout="wide"
)

# スタイルの定義
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 700px;
            margin: auto;
            padding: 1rem;
        }
        .chat-message {
            margin-bottom: 1rem;
            padding: 0.75rem 1rem;
            border-radius: 10px;
            width: fit-content;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #DCF8C6;
            margin-left: auto;
            text-align: left;
        }
        .bot-message {
            background-color: #F1F0F0;
            margin-right: auto;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 カウンセリングチャットボット v3")
st.markdown("""<div class="chat-container">""", unsafe_allow_html=True)

# セッション状態の初期化
if "history" not in st.session_state:
    st.session_state.history = []

# ユーザー入力の処理
user_input = st.chat_input("あなたの話したいことを自由に書いてください:")

if user_input:
    # ユーザーメッセージの追加
    st.session_state.history.append({"role": "user", "message": user_input})
    
    # AIの応答を取得
    result = app.invoke({
        "user_input": user_input,
        "conversation_history": [item["message"] for item in st.session_state.history if item["role"] == "user"]
    })
    response = result["response"]
    
    # AIの応答を履歴に追加
    st.session_state.history.append({"role": "bot", "message": response})

# 最新10件のメッセージを表示
for item in st.session_state.history[-10:]:
    if item["role"] == "user":
        st.markdown(f"""<div class='chat-message user-message'>{item['message']}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='chat-message bot-message'>{item['message']}</div>""", unsafe_allow_html=True)

st.markdown("""</div>""", unsafe_allow_html=True) 